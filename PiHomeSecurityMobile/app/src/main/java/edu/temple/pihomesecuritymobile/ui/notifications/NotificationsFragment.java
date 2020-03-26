package edu.temple.pihomesecuritymobile.ui.notifications;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.Bundle;
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
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import edu.temple.pihomesecuritymobile.R;

public class NotificationsFragment extends Fragment {

    private NotificationsViewModel notificationsViewModel;
    Context parent;
    onFragListener mList;
    final private int CAMERA_REQUEST_CODE = 22;
    final private int CAMERA_INTENT_CODE = 23;

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onAttach(Context context){
        super.onAttach(context);
        this.parent = context;
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

                            }
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

    public void openCamera() {
        Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(cameraIntent, CAMERA_INTENT_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_REQUEST_CODE) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(parent, "Camera permission granted", Toast.LENGTH_LONG).show();
                openCamera();
            } else {
                Toast.makeText(parent, "Camera permission denied", Toast.LENGTH_LONG).show();
            }
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == CAMERA_INTENT_CODE && resultCode == Activity.RESULT_OK) {
            //this is the photo the user took with camera, send to Pi in here
            Bitmap photo = (Bitmap) data.getExtras().get("data");
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