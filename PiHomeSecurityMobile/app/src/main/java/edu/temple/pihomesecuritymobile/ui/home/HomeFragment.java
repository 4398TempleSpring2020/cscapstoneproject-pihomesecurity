package edu.temple.pihomesecuritymobile.ui.home;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
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
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import org.json.JSONException;

import edu.temple.pihomesecuritymobile.MainActivity;
import edu.temple.pihomesecuritymobile.R;
import edu.temple.pihomesecuritymobile.models.Response;

public class HomeFragment extends Fragment {

    private HomeViewModel homeViewModel;
    Context parent;
    soundButtonListener mList;
    public HomeFragment(){

    }

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onAttach(Context context){
        super.onAttach(context);
        this.parent = context;
        if(context instanceof soundButtonListener){
            mList = (soundButtonListener) context;
        } else {
            throw new RuntimeException(context.toString() + "must implement soundButtonListener");
        }
    }


    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.fragment_home, container, false);
        final TextView textView = root.findViewById(R.id.text_home);
        textView.setText("Alarm Controller");
        final TextView alarmStr = root.findViewById(R.id.alarmStr);
        final Switch alarmSwitch = root.findViewById(R.id.alarmSwitch);
        final Button soundButton = root.findViewById(R.id.soundButtton);
        alarmSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if(b == true){
                    alarmStr.setText("Alarm: active");
                } else {
                    alarmStr.setText("Alarm: unactive");
                }
                mList.setAlarm(b);
            }
        });
        soundButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new AlertDialog.Builder(parent)
                        .setTitle("Confirm Action")
                        .setMessage("You are about to sound the panic alarm. Are you sure you want to continue?")
                        .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                mList.soundAlarm();
                            }
                        })
                        .setNegativeButton("Cancel", null)
                        .show();
            }
        });
        return root;
    }

    @Override
    public void onDetach(){
        super.onDetach();
        mList = null;
    }

    public interface soundButtonListener{
        public void soundAlarm();
        public void setAlarm(boolean setFlag);
    }
}