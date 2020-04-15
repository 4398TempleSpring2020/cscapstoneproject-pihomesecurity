package edu.temple.pihomesecuritymobile;

import android.content.Context;
import android.util.Log;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobile.config.AWSConfiguration;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferListener;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferObserver;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferState;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferUtility;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.CannedAccessControlList;

import java.io.File;

public class S3Manager {
    private Context context;
    final private String bucket = "mypishield";
    private String path;
    private String homeID;
    private CognitoCachingCredentialsProvider credentialsProvider;

    /**
     * constructor for S3Manager to set up context and homeID account
     * @param context
     * @param homeID
     */
    public S3Manager(Context context, String homeID) {
        this.context = context;
        this.homeID = homeID;
        credentialsProvider = new CognitoCachingCredentialsProvider(
                context.getApplicationContext(),
                "us-east-2:aac821c8-fb0d-4bda-a380-0fbeadb0f30d", // Identity pool ID
                Regions.US_EAST_2 // Region
        );

    }

    /**
     * upload a file to the S3
     * @param file to be uplaoded
     */
    public void upload(File file) {
        if (file != null) {
            AmazonS3 s3 = new AmazonS3Client(credentialsProvider);
            TransferUtility transferUtility = TransferUtility.builder()
                    .context(context)
                    .s3Client(s3)
                    .awsConfiguration(new AWSConfiguration(context))
                    .build();
            final TransferObserver observer = transferUtility.upload(
                    bucket,  //this is the bucket name on S3
                    homeID + "/faces/" + file.getName(), //this is the path and name
                    file //path to the file locally
            );
            observer.setTransferListener(new TransferListener() {
                @Override
                public void onStateChanged(int id, TransferState state) {
                    if (state.equals(TransferState.COMPLETED)) {
                        //Success
                    } else if (state.equals(TransferState.FAILED)) {
                        //Failed
                    }

                }

                @Override
                public void onProgressChanged(int id, long bytesCurrent, long bytesTotal) {

                }

                @Override
                public void onError(int id, Exception ex) {

                }
            });
        }
    }
}
