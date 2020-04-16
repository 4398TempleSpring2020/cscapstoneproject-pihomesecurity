package edu.temple.pihomesecuritymobile.ui.notifications;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.core.content.FileProvider;
import androidx.fragment.app.Fragment;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

import edu.temple.pihomesecuritymobile.R;
import edu.temple.pihomesecuritymobile.S3Manager;

public class NotificationsFragment extends Fragment {

    private NotificationsViewModel notificationsViewModel;
    Context parent;
    onFragListener mList;
    SharedPreferences sharePrefs;
    private String homeID;
    final private int CAMERA_REQUEST_CODE = 22;
    final private int CAMERA_INTENT_CODE = 23;
    final private int GALLERY_INTENT_CODE = 25;
    String currentPhotoPath;

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onAttach(Context context){
        super.onAttach(context);
        this.parent = context;
        sharePrefs = parent.getSharedPreferences("PREF_NAME",Context.MODE_PRIVATE);

        homeID = sharePrefs.getString("HomeID","");
        if(homeID.equals("")){
            Log.d("homeid err", "home id not found");
        }
        if(context instanceof onFragListener){
            mList = (onFragListener) context;
        } else {
            throw new RuntimeException(context.toString() + "must implement soundButtonListener");
        }
    }

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        View root = inflater.inflate(R.layout.fragment_notifications, container, false);
        final TextView textView = root.findViewById(R.id.text_notifications);
        textView.setText("Settings Menu");
        final Switch notoSwitch = root.findViewById(R.id.switch2);
        final TextView notoTell = root.findViewById(R.id.notoTell);
        notoSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if(b == true){
                    notoTell.setText("Notifactions: On");
                } else {
                    notoTell.setText("Notifications: Off");
                }
            }
        });
        //do photo stuff here
        Button button = root.findViewById(R.id.buttonPhotos);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new AlertDialog.Builder(parent, AlertDialog.THEME_TRADITIONAL)
                        .setTitle("Photo Upload")
                        .setMessage("Choose where to upload photo from")
                        //.setNeutralButton("Cancel", null)
                        .setNegativeButton("Gallery", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                Intent intent = new Intent();
                                intent.setType("image/*");
                                intent.setAction(Intent.ACTION_GET_CONTENT);
                                if (intent.resolveActivity(parent.getPackageManager()) != null) {
                                    startActivityForResult(Intent.createChooser(intent, "Select Picture"), GALLERY_INTENT_CODE);
                                }                            }
                        })
                        .setPositiveButton("Camera", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                //check permissions first
                                if (parent.checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                                    requestPermissions(new String[]{Manifest.permission.CAMERA}, CAMERA_REQUEST_CODE);
                                } else {
                                    openCamera();
                                }
                            }
                        })
                        .show();
            }
        });
        return root;
    }

    /**
     * open the camera on android
     * copied from android developer guide
     */
    public void openCamera() {
        Toast.makeText(parent, "Opening camera", Toast.LENGTH_LONG).show();
        Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        File photoFile = null;
        try {
            photoFile = createImageFile();
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        // Continue only if the File was successfully created
        if (photoFile != null) {
            Uri photoURI = FileProvider.getUriForFile(parent,
                    "edu.temple.pihomesecuritymobile.fileprovider",
                    photoFile);
            cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
            startActivityForResult(cameraIntent, CAMERA_INTENT_CODE);
        }
    }

    /**
     * Creates a temporary file to store the image taken with the camera so we can get a full sized image
     * copied from android developer guide
     * @return the image file
     * @throws IOException
     */
    private File createImageFile() throws IOException {
        // Create an image file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = parent.getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        // Save a file: path for use with ACTION_VIEW intents
        currentPhotoPath = image.getAbsolutePath();
        return image;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_REQUEST_CODE) {
            //user said yes to camera use
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(parent, "Camera permission granted", Toast.LENGTH_LONG).show();
                openCamera();
            } else {
                //user said no to camera use
                Toast.makeText(parent, "Camera permission denied", Toast.LENGTH_LONG).show();
            }
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == CAMERA_INTENT_CODE && resultCode == Activity.RESULT_OK) {
            //Bitmap photo = (Bitmap) data.getExtras().get("data");
            try {
                File file = new File(currentPhotoPath);
                S3Manager s3Manager = new S3Manager(parent, homeID);
                Toast.makeText(parent, "Uploading photo to Raspberry Pi", Toast.LENGTH_LONG).show();
                s3Manager.upload(file);
                //Bitmap bitmap = MediaStore.Images.Media.getBitmap(parent.getContentResolver(), Uri.fromFile(file));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        if (requestCode == GALLERY_INTENT_CODE && resultCode == Activity.RESULT_OK) {
            try {
                File file = null;
                try {
                    file = createImageFile();
                } catch (IOException ex) {
                    Log.d("error gallery", "Error occurred while creating the file");
                }
                InputStream inputStream = getActivity().getContentResolver().openInputStream(data.getData());
                FileOutputStream fileOutputStream = new FileOutputStream(file);
                // copy image to new file so we can send it to the S3
                copyStream(inputStream, fileOutputStream);
                fileOutputStream.close();
                inputStream.close();
                S3Manager s3Manager = new S3Manager(parent, homeID);
                Toast.makeText(parent, "Uploading photo to Raspberry Pi", Toast.LENGTH_LONG).show();
                s3Manager.upload(file);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

    }

    /**
     * reads from one stream and writes to another stream
     * @param input stream to read from
     * @param output stream to write to
     * @throws IOException
     */
    public static void copyStream(InputStream input, OutputStream output) throws IOException {
        byte[] buffer = new byte[1024];
        int bytesRead;
        while ((bytesRead = input.read(buffer)) != -1) {
            output.write(buffer, 0, bytesRead);
        }
    }

    @Override
    public void onDetach(){
        super.onDetach();
        mList = null;
    }

    public interface onFragListener{

    }
}