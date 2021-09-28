const fs = require("fs");
const {
    Logger,
    SmartlingApiClientBuilder,
    SmartlingJobsApi,
    SmartlingJobBatchesApi,
    SmartlingFilesApi,
    CreateJobParameters,
    CreateBatchParameters,
    UploadBatchFileParameters,
    FileType,
    JobProgressParameters,
    DownloadFileParameters,
    RetrievalType
} = require("smartling-api-sdk-nodejs");

const projectId = process.env.DEV_PROJECT_ID;
const userId = process.env.DEV_USER_IDENTIFIER;
const userSecret = process.env.DEV_USER_SECRET;

if (!projectId || !userId || !userSecret) {
    console.error("Missing environment variables. Did you run setenv?");

    process.exit(1);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Create factory for building API clients.
const apiBuilder = new SmartlingApiClientBuilder()
    .setLogger(console)
    .setBaseSmartlingApiUrl("https://api.smartling.com")
    .setClientLibMetadata("translating-with-jobs-tutorial-nodejs", "1.0.0")
    .setHttpClientConfiguration({
        timeout: 10000
    })
    .authWithUserIdAndUserSecret(userId, userSecret);

// Instantiate the APIs we'll need.
const jobsApi = apiBuilder.build(SmartlingJobsApi);
const batchesApi = apiBuilder.build(SmartlingJobBatchesApi);
const filesApi = apiBuilder.build(SmartlingFilesApi);
const locale = "fr-FR";

(async () => {
    try {
        // Create job.
        const createJobParams = new CreateJobParameters()
            .setName(`Test job name ${Date.now()}`)
            .setDescription("Test job description");

        console.log("Calling 'create job' endpoint...");

        const job = await jobsApi.createJob(projectId, createJobParams);

        console.log(`Job created. Job ID: ${job.translationJobUid}`);

        // Generate URIs for the test files.
        // For testing purposes, we're prepending the job ID to the file names to generate a unique
        // URI for each run of the test, thus allowing the same file to be added to different jobs.
        const filesList = [
            "data/file_1.xml",
            "data/file_2.xml"
        ];
        const filesInfo = filesList
            .map(fileName => ({
                fileName,
                fileUri: `${job.translationJobUid}/${fileName}`
            }));

        // Create job batch.
        const createBatchParams = new CreateBatchParameters()
            .setTranslationJobUid(job.translationJobUid)
            .setAuthorize(true);

        filesInfo
            .forEach(
                fileInfo => createBatchParams.addFileUri(fileInfo.fileUri)
            );

        console.log("Calling 'create job batch' endpoint...");

        const batch = await batchesApi.createBatch(projectId, createBatchParams);

        console.log(`Job batch created. Batch ID ${batch.batchUid}`);

        // Add files to batch.
        console.log("Calling 'upload file to batch' endpoint...");

        for (const fileInfo of filesInfo) {
            const uploadBatchFileParams = new UploadBatchFileParameters()
                .setFile(fileInfo.fileName)
                .setFileUri(fileInfo.fileUri)
                .setFileType(FileType.XML)
                .setLocalesToApprove([locale]);

            await batchesApi.uploadBatchFile(projectId, batch.batchUid, uploadBatchFileParams);

            console.log(`Added file ${fileInfo.fileName}`);
        }

        console.log("Finished adding files to batch");

        // Check job status until complete.
        console.log("Will check job status every 10 seconds");

        let percentComplete = 0;

        do {
            await sleep(10000);

            const jobProgressParams = new JobProgressParameters()
                .setTargetLocaleId(locale);

            const jobProgress = await jobsApi.getJobProgress(projectId, job.translationJobUid, jobProgressParams);

            percentComplete = jobProgress.progress.percentComplete;

            console.log(`Job Progress: ${percentComplete}%`);
        }
        while (percentComplete < 100);

        console.log("Job is complete; downloading translated files...");

        // Download translated files.
        for (const fileInfo of filesInfo) {
            const downloadFileParams = new DownloadFileParameters()
                .setRetrievalType(RetrievalType.PUBLISHED);

            const downloadedFileContent = await filesApi.downloadFile(projectId, fileInfo.fileUri, locale, downloadFileParams);

            fs.writeFileSync(`${locale}_${fileInfo.fileUri}`.replace(/\//g, "_"), downloadedFileContent);

            console.log(`Downloaded ${fileInfo.fileUri}`);
        }
    } catch (e) {
        console.error(e);
    }
})();
