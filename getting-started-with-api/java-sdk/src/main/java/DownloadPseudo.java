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
import java.io.InputStream;
import static java.nio.charset.StandardCharsets.UTF_8;

public class DownloadPseudo
{
    public static void main( String[] args ) throws Exception
    {
        // Read command-line arguments
        if (args.length != 2) {
            System.out.println("Usage: mvn -X exec:java -Dexec.mainClass=\"DownloadPseudo\" -Dexec.args=\"<fileUri> <localeId>\"");
            System.out.println("E.g.: mvn -X exec:java -Dexec.mainClass=\"DownloadPseudo\" -Dexec.args=\"strings.json fr-FR\"");
            System.out.println("Takes two command-line parameters: ");
            System.out.println("  fileUri: URI in Smartling of the file to be downloaded");
            System.out.println("  localeId: any locale ID that is defined in the Smartling project");
            System.exit(1);
        }
        String fileUri = args[0];
        String localeId = args[1];

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
            System.out.println("\nContents of downloaded file: \n");
            System.out.println(IOUtils.toString(translatedFile, UTF_8.name()));
            // todo: write to file (is this stream fully in memory or potentially still being downloaded?
        } catch  (RestApiRuntimeException e) {
            System.out.println(e.getMessage());
        }
    }

}
