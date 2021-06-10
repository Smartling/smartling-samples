package com.smartling.samples.gettingstarted;

import com.smartling.api.files.v2.FilesApi;
import com.smartling.api.files.v2.FilesApiFactory;
import com.smartling.api.files.v2.pto.DownloadTranslationPTO;
import com.smartling.api.files.v2.pto.RetrievalType;
import com.smartling.api.v2.authentication.AuthenticationApi;
import com.smartling.api.v2.authentication.AuthenticationApiFactory;
import com.smartling.api.v2.client.ClientFactory;
import com.smartling.api.v2.client.DefaultClientConfiguration;
import com.smartling.api.v2.client.auth.Authenticator;
import com.smartling.api.v2.client.auth.BearerAuthSecretFilter;
import com.smartling.api.v2.client.exception.RestApiRuntimeException;
import org.apache.commons.io.IOUtils;
import org.apache.commons.io.FileUtils;
import java.io.InputStream;
import java.io.File;
import static java.nio.charset.StandardCharsets.UTF_8;

public class DownloadPseudo
{
    public static void main( String[] args ) throws Exception
    {
        // Read command-line arguments
        if (args.length != 3) {
            System.out.println("Usage: mvn -q exec:java@download");
            System.out.println("(See pom.xml to configure parameters.)");
            System.exit(1);
        }
        String fileUri = args[0];
        String outputFileName = args[1];
        String localeId = args[2];

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

        // Create files API client
        FilesApi filesApi = new FilesApiFactory(clientFactory)
            .buildApi(new BearerAuthSecretFilter(authenticator), clientConfiguration);

        // Build the API request
        DownloadTranslationPTO downloadTranslationPTO = DownloadTranslationPTO.builder()
            .fileUri(fileUri)
            .retrievalType(RetrievalType.PSEUDO)
            .build();

        // Execute the download
        try {
            InputStream translatedFile = filesApi.downloadTranslatedFile(projectId, localeId, downloadTranslationPTO);
            System.out.println();
            System.out.println("Downloaded file: " + outputFileName);
            System.out.println();
            File outputFile = new File(outputFileName);
            FileUtils.copyInputStreamToFile(translatedFile, outputFile);
        } catch  (RestApiRuntimeException e) {
            System.err.println();
            System.err.println("Download failed. Response details:");
            System.err.println(e.getMessage());
            System.err.println();
        }
    }

}
