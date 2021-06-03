import com.smartling.api.files.v2.FilesApi;
import com.smartling.api.files.v2.FilesApiFactory;
import com.smartling.api.files.v2.pto.FileType;
import com.smartling.api.files.v2.pto.UploadFilePTO;
import com.smartling.api.files.v2.pto.UploadFileResponse;
import com.smartling.api.v2.authentication.AuthenticationApi;
import com.smartling.api.v2.authentication.AuthenticationApiFactory;
import com.smartling.api.v2.client.ClientFactory;
import com.smartling.api.v2.client.DefaultClientConfiguration;
import com.smartling.api.v2.client.auth.Authenticator;
import com.smartling.api.v2.client.auth.BearerAuthSecretFilter;
import com.smartling.api.v2.client.exception.RestApiRuntimeException;

import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Upload
{
    private static final List<String> locales = new ArrayList<>(Arrays.asList("fr-FR"));

    public static void main( String[] args ) throws Exception
    {
        // Read command-line arguments
        if (args.length != 2) {
            System.out.println("Usage: mvn -X exec:java -Dexec.mainClass=\"Upload\" -Dexec.args=\"<fileName> <fileType>\"");
            System.out.println("E.g.: mvn -X exec:java -Dexec.mainClass=\"Upload\" -Dexec.args=\"strings.json json\"");
            System.out.println("Takes two command-line parameters: ");
            System.out.println("  fileName: local name of file to be uploaded");
            System.out.println("  fileType: file type of file to be uploaded");
            System.exit(1);
        }
        String fileName = args[0];
        String fileType = args[1];

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
        UploadFilePTO uploadFilePto = UploadFilePTO.builder()
            .file(new FileInputStream(fileName))
            .fileUri(fileName)
            .fileType(FileType.lookup(fileType))
            .localeIdsToAuthorize(locales)
            .build();

        // Execute the upload
        try {
            UploadFileResponse uploadFileResponse = filesApi.uploadFile(projectId, uploadFilePto);
            System.out.println(uploadFileResponse);
        } catch (RestApiRuntimeException e) {
            System.out.println(e.getMessage());
        }
    }

}
