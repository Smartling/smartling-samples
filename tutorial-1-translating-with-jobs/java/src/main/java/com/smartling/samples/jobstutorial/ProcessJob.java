package com.smartling.samples.jobstutorial;

import com.smartling.api.files.v2.FilesApi;
import com.smartling.api.files.v2.FilesApiFactory;
import com.smartling.api.files.v2.pto.DownloadTranslationPTO;
import com.smartling.api.files.v2.pto.RetrievalType;
import com.smartling.api.jobbatches.v2.JobBatchesApi;
import com.smartling.api.jobbatches.v2.JobBatchesApiFactory;
import com.smartling.api.jobbatches.v2.pto.CreateBatchRequestPTO;
import com.smartling.api.jobbatches.v2.pto.CreateBatchResponsePTO;
import com.smartling.api.jobbatches.v2.pto.StreamFileUploadPTO;
import com.smartling.api.jobs.v3.TranslationJobsApi;
import com.smartling.api.jobs.v3.TranslationJobsApiFactory;
import com.smartling.api.jobs.v3.pto.ContentProgressReportPTO;
import com.smartling.api.jobs.v3.pto.TranslationJobCreateCommandPTO;
import com.smartling.api.jobs.v3.pto.TranslationJobCreateResponsePTO;
import com.smartling.api.v2.authentication.AuthenticationApi;
import com.smartling.api.v2.authentication.AuthenticationApiFactory;
import com.smartling.api.v2.client.ClientFactory;
import com.smartling.api.v2.client.DefaultClientConfiguration;
import com.smartling.api.v2.client.auth.Authenticator;
import com.smartling.api.v2.client.auth.BearerAuthSecretFilter;
import com.smartling.api.v2.client.exception.RestApiRuntimeException;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;


public class ProcessJob
{
    private static final List<String> LOCALES = new ArrayList<>(Arrays.asList("fr-FR"));
    private static final List<String> FILE_LIST = new ArrayList<>(Arrays.asList("site-navigation.json","products.json"));
    private static final String FILE_TYPE = "json";

    public static void main( String[] args ) throws Exception
    {
        // Read command-line arguments
        if (args.length != 1) {
            System.out.println("Usage: mvn exec:java@run");
            System.out.println("(See pom.xml to configure parameters.)");
            System.exit(1);
        }
        String jobName = args[0];

        // Read authentication credentials from environment
        String userId = System.getenv("DEV_USER_IDENTIFIER");
        String userSecret = System.getenv("DEV_USER_SECRET");
        String projectId = System.getenv("DEV_PROJECT_ID");
        if (userId == null || userSecret == null || projectId == null) {
            System.out.println("Missing environment variables. Did you run setenv?");
            System.exit(1);
        }

        // Create factory for building API clients
        DefaultClientConfiguration clientConfiguration = DefaultClientConfiguration.builder().build();
        ClientFactory clientFactory = new ClientFactory();

        // Create the authenticator to be used by subsequent API calls
        AuthenticationApi authenticationApi = new AuthenticationApiFactory(clientFactory).buildApi(clientConfiguration);
        Authenticator authenticator = new Authenticator(userId, userSecret, authenticationApi);

        try {
            System.out.println();

            // create job
            System.out.println("Calling 'create job' endpoint...");
            TranslationJobsApi jobsApi = new TranslationJobsApiFactory(clientFactory)
                    .buildApi(new BearerAuthSecretFilter(authenticator), clientConfiguration);
            String jobUid = createJob(jobsApi, projectId, jobName);
            System.out.println("Job created. Job ID: " + jobUid);

            // create job batch
            System.out.println("Calling 'create job batch' endpoint...");
            JobBatchesApi jobBatchesApi = new JobBatchesApiFactory(clientFactory)
                    .buildApi(new BearerAuthSecretFilter(authenticator), clientConfiguration);
            String batchUid = createJobBatch(jobBatchesApi, projectId, jobUid);
            System.out.println("Job batch created. Batch ID: " + batchUid);

            // add files to batch
            System.out.println("Calling 'upload file to batch' endpoint...");
            for (String fileName : FILE_LIST) {
                String fileUri = getUriFromFileName(jobUid, fileName);
                addFileToBatch(jobBatchesApi, projectId, batchUid, fileName, fileUri);
                System.out.println("Added file " + fileName);
            }
            System.out.println("Finished adding files to batch");

            // checking job status until complete
            System.out.println("Will check job status every 10 seconds");
            int percentComplete = 0;
            do {
                TimeUnit.SECONDS.sleep(10);
                ContentProgressReportPTO response = jobsApi.getTranslationJobProgress(projectId, jobUid, "");
                percentComplete = response.getProgress().getPercentComplete();
                System.out.println("Job Progress: " + percentComplete  + "%");
            }
            while (percentComplete < 100);
            System.out.println("Job is complete; downloading translated files...");

            // download translated files
            FilesApi filesApi = new FilesApiFactory(clientFactory)
                    .buildApi(new BearerAuthSecretFilter(authenticator), clientConfiguration);
            for (String fileName : FILE_LIST) {
                String fileUri = getUriFromFileName(jobUid, fileName);
                for (String locale : LOCALES) {
                    InputStream translations = downloadTranslatedFile(filesApi, projectId, fileUri, locale);
                    String outputFileName = getOutputFileName(fileName, locale);
                    File outputFile = new File(outputFileName);
                    FileUtils.copyInputStreamToFile(translations, outputFile);
                    System.out.println("Downloaded " + outputFileName);
                }
            }

        } catch (RestApiRuntimeException e) {
            System.err.println("Request error. Response details:");
            System.err.println(e.getMessage());
            System.err.println();
        }

    }

    public static String createJob(TranslationJobsApi jobsApi, String projectId, String jobName) throws RestApiRuntimeException
    {
        TranslationJobCreateCommandPTO requestBody = TranslationJobCreateCommandPTO.builder()
                .jobName(jobName)
                .build();

        TranslationJobCreateResponsePTO response = jobsApi.createTranslationJob(projectId, requestBody);

        return response.getTranslationJobUid();
    }


    public static String createJobBatch(JobBatchesApi jobBatchesApi, String projectId, String jobUid) throws RestApiRuntimeException
    {
        CreateBatchRequestPTO requestBody = CreateBatchRequestPTO.builder()
                .translationJobUid(jobUid)
                .authorize(true)
                .fileUris(getUris(jobUid)) // prepend jobUid to file URI to avoid confusion during testing
                .build();

        CreateBatchResponsePTO response = jobBatchesApi.createBatch(projectId, requestBody);

        return response.getBatchUid();
    }

    public static void addFileToBatch(JobBatchesApi jobBatchesApi, String projectId, String batchUid, String fileName, String fileUri) throws RestApiRuntimeException, FileNotFoundException
    {
        StreamFileUploadPTO requestBody = StreamFileUploadPTO.builder()
                .fileUri(fileUri)
                .fileType(FILE_TYPE)
                .localeIdsToAuthorize(LOCALES)
                .file(new FileInputStream(fileName))
                .build();

        jobBatchesApi.addFileAsStreamAsync(projectId, batchUid, requestBody);

    }

    public static InputStream downloadTranslatedFile(FilesApi filesApi, String projectId, String fileUri, String localeId) throws RestApiRuntimeException
    {
        DownloadTranslationPTO requestBody = DownloadTranslationPTO.builder()
                .fileUri(fileUri)
                .retrievalType(RetrievalType.PUBLISHED)
                .build();

        return filesApi.downloadTranslatedFile(projectId, localeId, requestBody);

    }

    static String getOutputFileName(String fileName, String locale) {
        // return file names of the form <filename>_<locale>.<extension>
        int dotIndex = fileName.lastIndexOf('.');
        return fileName.substring(0, dotIndex) + "_" + locale + fileName.substring(dotIndex);
    }


    // For the test script, we're prepending the job ID to the file URIs, allowing the
    // same file to be uploaded to different jobs, since URIs will be different.
    static List getUris(String jobUid) {
        List uris = new ArrayList();
        for (String fileName : FILE_LIST) {
            uris.add(getUriFromFileName(jobUid, fileName));
        }
        return uris;
    }

    static String getUriFromFileName(String jobUid, String fileName) {
        return jobUid + "/" + fileName;
    }
}
