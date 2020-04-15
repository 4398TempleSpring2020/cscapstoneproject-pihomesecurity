package edu.temple.awsapi;

import android.content.Context;
import android.widget.Toast;

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
import com.amazonaws.services.s3.model.ObjectListing;

import java.io.File;

public class S3Manager {
    private Context c;
    public void uploadtos3 (Context context, File file) {
        c = context;
        if(file !=null){
            CognitoCachingCredentialsProvider credentialsProvider;
            credentialsProvider = new CognitoCachingCredentialsProvider(
                    context.getApplicationContext(),
                    "us-east-2:aac821c8-fb0d-4bda-a380-0fbeadb0f30d", // Identity pool ID
                    Regions.US_EAST_2 // Region
            );

            AmazonS3 s3 = new AmazonS3Client(credentialsProvider);
            TransferUtility transferUtility = TransferUtility.builder()
                    .context(context)
                    .s3Client(s3)
                    .awsConfiguration(new AWSConfiguration(context))
                    .build();
            final TransferObserver observer = transferUtility.upload(
                    "whateverworks",  //this is the bucket name on S3
                    file.getName(),
                    file
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
