package edu.temple.awsapi;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity implements ContentManager.AsyncListener {
    private TextView textView;
    protected static Response response = new Response();
    final private int CAMERA_REQUEST_CODE = 22;
    final private int CAMERA_INTENT_CODE = 23;
    public static final int GALLERY_INTENT_CODE = 25;
    String currentPhotoPath;

    ImageView imageView;
    ImageView imageView2;
    // protected Map<String,String> params = new HashMap<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //textView = findViewById(R.id.textview1);
        //get only returns the name of each table
        //ContentManager contentManager = new ContentManager(this);
        //contentManager.showTables();
        //contentManager.selectStatement("Employee", "*");
        //contentManager.selectIDStatement("Employee", "*", "EmployeeID", "1");
        //contentManager.insertStatement("Employee", "EmployeeName, EmployeeUsername, EmployeePassword", "'Temple Employee 3', 'TUID 3', '1234'");
        //contentManager.deleteStatement("Employee", "EmployeeID", "15");
        //contentManager.updateStatement("Employee", "Employee Name", "'New Employee'", "EmployeeID", "1");
        Button button = findViewById(R.id.button);
        imageView = findViewById(R.id.imageView3);
        imageView2 = findViewById(R.id.imageView4);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new AlertDialog.Builder(MainActivity.this, AlertDialog.THEME_TRADITIONAL)
                        .setTitle("Photo Upload")
                        .setMessage("Choose where to upload photo from")
                        //.setNeutralButton("Cancel", null)
                        .setNegativeButton("Gallery", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                Intent intent = new Intent();
                                intent.setType("image/*");
                                intent.setAction(Intent.ACTION_GET_CONTENT);
                                if (intent.resolveActivity(getPackageManager()) != null) {
                                    startActivityForResult(Intent.createChooser(intent, "Select Picture"), GALLERY_INTENT_CODE);
                                }
                            }
                        })
                        .setPositiveButton("Camera", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                                    requestPermissions(new String[]{Manifest.permission.CAMERA}, CAMERA_REQUEST_CODE);
                                } else {
                                    openCamera();
                                }
                            }
                        })

                        .show();
            }
        });

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_REQUEST_CODE) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Camera permission granted", Toast.LENGTH_LONG).show();
                openCamera();
            } else {
                Toast.makeText(this, "Camera permission denied", Toast.LENGTH_LONG).show();
            }
        }
    }

    private File createImageFile() throws IOException {
        // Create an image file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        // Save a file: path for use with ACTION_VIEW intents
        currentPhotoPath = image.getAbsolutePath();
        return image;
    }

    public void openCamera() {
        Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        //startActivityForResult(cameraIntent, CAMERA_INTENT_CODE);
        File photoFile = null;
        try {
            photoFile = createImageFile();
        } catch (IOException ex) {
            // Error occurred while creating the File

        }
        // Continue only if the File was successfully created
        if (photoFile != null) {
            Uri photoURI = FileProvider.getUriForFile(this,
                    "edu.temple.awsapi.fileprovider",
                    photoFile);
            cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
            startActivityForResult(cameraIntent, CAMERA_INTENT_CODE);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == CAMERA_INTENT_CODE && resultCode == Activity.RESULT_OK) {
            //Bitmap photo = (Bitmap) data.getExtras().get("data");
            //imageView.setImageBitmap(photo);
            try {
                File file = new File(currentPhotoPath);
                S3Manager s3Manager = new S3Manager();
                s3Manager.uploadtos3(this, file);
                Bitmap bitmap = MediaStore.Images.Media.getBitmap(MainActivity.this.getContentResolver(), Uri.fromFile(file));
                if (bitmap != null) {
                    imageView.setImageBitmap(bitmap);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        if (requestCode == GALLERY_INTENT_CODE && resultCode == Activity.RESULT_OK) {
            try {
                Uri fullPhotoUri = data.getData();
                imageView2.setImageURI(fullPhotoUri);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

    }

    /**
     * put stuff in here that you want to happen after Async network stuff done.
     * Get data from POST this way.
     * @param nresponse: Response object holding response data
     */
    public void doAfterAsync(Response nresponse) {
        response=nresponse;
        Log.d("STATUSCODE", "status code: " + response.getStatusCode());
        Log.d("MESSAGE", "message: " + response.getMessage());
        Log.d("RESPONSE", "body: " + response.getBodyString());
    }
}


