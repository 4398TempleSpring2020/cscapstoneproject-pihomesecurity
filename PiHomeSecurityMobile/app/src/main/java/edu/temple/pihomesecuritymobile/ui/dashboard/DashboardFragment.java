package edu.temple.pihomesecuritymobile.ui.dashboard;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProviders;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.EmptyStackException;
import java.util.concurrent.TimeUnit;

import edu.temple.pihomesecuritymobile.ContentManager;
import edu.temple.pihomesecuritymobile.ImageViewer;
import edu.temple.pihomesecuritymobile.IncidentImageAdapter;
import edu.temple.pihomesecuritymobile.R;
import edu.temple.pihomesecuritymobile.models.Response;

public class DashboardFragment extends Fragment {

    private DashboardViewModel dashboardViewModel;
    String errMess;
    SharedPreferences sharePrefs;
    Response rsp;
    ContentManager mngr;
    JSONObject dataObj;
    Context parent;
    onFragListener mList;
    private String home_ID;
    private String current_username;
    private String incDate;
    private String IDstr;
    private final long SECONDS_DIFF = 300; //5 minutes

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onAttach(Context context){
        super.onAttach(context);
        this.parent = context;
        sharePrefs = parent.getSharedPreferences("PREF_NAME",Context.MODE_PRIVATE);
        mngr = new ContentManager();
        // Place API code to get data to display
        String HomeID = sharePrefs.getString("HomeID","");
        current_username = sharePrefs.getString("UserName", "");
        Log.d("username", "" + current_username);
        if(HomeID.equals("")){
            errMess = "HomeID was not found";
        } else {
            String result = mngr.getIncidents(HomeID);
            Log.d("homeID", "" + HomeID);
            home_ID=HomeID;
            Log.d("incidents result", "" + result);
            rsp = mngr.makeResponse(result);
        }

        if(rsp.getStatusCode()==mngr.records_not_exist){
            errMess = "Records do not exist";
        } else {
            dataObj = rsp.getBody();
            Log.d("JSONObject", dataObj.toString());
        }

        if(context instanceof onFragListener){
            mList = (onFragListener) context;
        } else {
            throw new RuntimeException(context.toString() + "must implement soundButtonListener");
        }
    }

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        dashboardViewModel =
                ViewModelProviders.of(this).get(DashboardViewModel.class);
        final View root = inflater.inflate(R.layout.fragment_dashboard, container, false);
        final TextView textView = root.findViewById(R.id.text_dashboard);
        textView.setText("Incidents");
        final TextView incID = root.findViewById(R.id.textView2);
        TextView occDate = root.findViewById(R.id.textView3);
        GridView gridView = root.findViewById(R.id.gridViewInc);
        int set = 0;

        final Button escalateButton = root.findViewById(R.id.escalate);
        final Button resolveButton = root.findViewById(R.id.resolve);

        escalateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new AlertDialog.Builder(parent)
                        .setTitle("Confirm Action")
                        .setMessage("You are about to escalate this incident which will contact the authorities. Are you sure you want to continue?")
                        .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                //we need to check that more than the predetermined amount of time has not passed
                                //and that authorities were not contacted already
                                long seconds = getSecondsDiff();
                                String result2 = mngr.selectIDStatement("IncidentData", "EmergencyContactedFlag, BadIncidentFlag", "IncidentID", IDstr);
                                Response response2 = mngr.makeResponse(result2);

                                int authoritiesContacted = 0;
                                int badIncident = 1;
                                try {
                                    authoritiesContacted = response2.getBody().getInt("EmergencyContactedFlag");
                                    badIncident = response2.getBody().getInt("BadIncidentFlag");
                                    Log.d("BadIncidentFlag", "" + badIncident);
                                    Log.d("authorities_flag", "" + authoritiesContacted);
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                if (seconds <= SECONDS_DIFF && seconds>=0 && authoritiesContacted==0 && badIncident==1) {
                                    mList.escalateRsp();
                                    mngr.alertResponse(home_ID, "yes");
                                    Toast.makeText(parent.getApplicationContext(), "Sending escalation response.", Toast.LENGTH_SHORT).show();
                                } else if (seconds > SECONDS_DIFF || authoritiesContacted == 1 || badIncident == 0) {
                                    resolveButton.setClickable(false);
                                    resolveButton.setAlpha(0.3f);
                                    escalateButton.setClickable(false);
                                    escalateButton.setAlpha(0.3f);
                                    String message;
                                    if (seconds>SECONDS_DIFF) {
                                        message = "More than " + SECONDS_DIFF/60 + " minutes have passed since the incident occurred. Your response cannot be recorded.";
                                    } else if (authoritiesContacted==1){
                                        message = "Authorities were already contacted. Your response cannot be recorded.";
                                    } else {
                                        message = "This incident was already marked as resolved. Your response cannot be recorded.";
                                    }
                                    Toast.makeText(parent.getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                                    new AlertDialog.Builder(parent)
                                            .setTitle("Alert")
                                            .setMessage(message)
                                            .setNeutralButton("Ok", null)
                                            .show();
                                } else {
                                    Toast.makeText(parent.getApplicationContext(), "Something went wrong.", Toast.LENGTH_SHORT).show();
                                    Log.e("error", "Something went wrong.");
                                }
                            }
                        })
                        .setNegativeButton("Cancel", null)
                        .show();
            }
        });

        resolveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new AlertDialog.Builder(parent)
                        .setTitle("Confirm Action")
                        .setMessage("You are about to mark this incident as resolved. Are you sure you want to continue?")
                        .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                //we need to check that more than the predetermined amount of time has not passed
                                //and that authorities were not contacted already
                                long seconds = getSecondsDiff();
                                String result2 = mngr.selectIDStatement("IncidentData", "EmergencyContactedFlag, BadIncidentFlag", "IncidentID", IDstr);
                                Response response2 = mngr.makeResponse(result2);

                                int authoritiesContacted = 0;
                                int badIncident = 1;
                                try {
                                    authoritiesContacted = response2.getBody().getInt("EmergencyContactedFlag");
                                    badIncident = response2.getBody().getInt("BadIncidentFlag");
                                    Log.d("BadIncidentFlag", "" + badIncident);
                                    Log.d("authorities_flag", "" + authoritiesContacted);
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                                if (seconds <= SECONDS_DIFF && seconds>=0 && authoritiesContacted==0 && badIncident==1) {
                                    mList.resolveRsp();
                                    mngr.alertResponse(home_ID, "no");
                                    Toast.makeText(parent.getApplicationContext(), "Sending de-escalation response.", Toast.LENGTH_SHORT).show();
                                } else if (seconds > SECONDS_DIFF || authoritiesContacted == 1 || badIncident == 0) {
                                    resolveButton.setClickable(false);
                                    resolveButton.setAlpha(0.3f);
                                    escalateButton.setClickable(false);
                                    escalateButton.setAlpha(0.3f);
                                    String message;
                                    if (seconds>SECONDS_DIFF) {
                                        message = "More than " + SECONDS_DIFF/60 + " minutes have passed since the incident occurred. Your response cannot be recorded.";
                                    } else if (authoritiesContacted==1){
                                        message = "Authorities were already contacted. Your response cannot be recorded.";
                                    } else {
                                        message = "This incident was already marked as resolved. Your response cannot be recorded.";
                                    }
                                    Toast.makeText(parent.getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                                    new AlertDialog.Builder(parent)
                                            .setTitle("Alert")
                                            .setMessage(message)
                                            .setNeutralButton("Ok", null)
                                            .show();
                                } else {
                                    Toast.makeText(parent.getApplicationContext(), "Something went wrong.", Toast.LENGTH_SHORT).show();
                                    Log.e("error", "Something went wrong.");
                                }
                            }
                        })
                        .setNegativeButton("Cancel", null)
                        .show();
            }
        });

        if (dataObj!=null) { //no incidents exist yet
            set = 1;
        }
        try{
            if (set == 0) {
                incID.setText("No Incident data available.");
                occDate.setText("");
                resolveButton.setAlpha(0);
                resolveButton.setClickable(false);
                escalateButton.setAlpha(0);
                escalateButton.setClickable(false);
            } else if(set == 1){
                IDstr = dataObj.getString("IncidentID");
                incID.setText( "Incident ID: " + IDstr);
                Log.d("incidentID", "" + IDstr);
                incDate = dataObj.getString("DateRecorded");
                occDate.setText("Incident occurred at: " + incDate);
                mngr.updateStatement("IncidentData", "LastAccessed", "current_timestamp()", "IncidentID", IDstr);
                if (current_username!=null) {
                    mngr.updateStatement("IncidentData", "UserAccessed", current_username, "IncidentID", IDstr);
                }

                String paths = dataObj.getString("ImagePaths");
                Log.d("paths", "" + paths);
                final String[] imagePaths = paths.split(",");
                IncidentImageAdapter incidentImageAdapter = new IncidentImageAdapter(parent, imagePaths);
                gridView.setAdapter(incidentImageAdapter);
                gridView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                        // Send intent to SingleViewActivity
                        Intent i = new Intent(root.getContext(), ImageViewer.class);
                        // Pass image index
                        i.putExtra("image_id", position);
                        i.putExtra("images", imagePaths);
                        i.putExtra("home_id", home_ID);
                        startActivity(i);
                    }
                });

                //determine if we should let user click the response buttons
                long seconds = getSecondsDiff();
                String result2 = mngr.selectIDStatement("IncidentData", "EmergencyContactedFlag, BadIncidentFlag", "IncidentID", IDstr);
                Response response2 = mngr.makeResponse(result2);

                int authoritiesContacted = 0;
                int badIncident = 1;
                try {
                    authoritiesContacted = response2.getBody().getInt("EmergencyContactedFlag");
                    badIncident = response2.getBody().getInt("BadIncidentFlag");

                } catch (JSONException e) {
                    e.printStackTrace();
                }
                if (seconds > SECONDS_DIFF || authoritiesContacted == 1 || badIncident == 0) {
                    resolveButton.setClickable(false);
                    resolveButton.setAlpha(0.3f);
                    escalateButton.setClickable(false);
                    escalateButton.setAlpha(0.3f);
                } else if (seconds <= SECONDS_DIFF && seconds >= 0 && authoritiesContacted==0 && badIncident==1) {
                    resolveButton.setClickable(true);
                    resolveButton.setAlpha(1);
                    escalateButton.setClickable(true);
                    escalateButton.setAlpha(1);
                } else {
                    resolveButton.setClickable(false);
                    resolveButton.setAlpha(0.3f);
                    escalateButton.setClickable(false);
                    escalateButton.setAlpha(0.3f);
                    Log.e("error", "Something went wrong determining time difference...");
                }
            }
        } catch(JSONException e){
            incID.setText(errMess);
            occDate.setText("");
        }

        return root;
    }

    @Override
    public void onDetach(){
        super.onDetach();
        mList = null;
    }

    public interface onFragListener{
        void escalateRsp();
        void resolveRsp();
    }

    /**
     * gets the difference between incident date and current date in seconds
     * @return seconds between the two dates
     */
    public long getSecondsDiff() {
        try {
            Date currentDate = Calendar.getInstance().getTime();
            SimpleDateFormat df = new SimpleDateFormat("MM-dd-yyyy HH:mm:ss");
            String formattedDate = df.format(currentDate);
            Log.d("current time", "" + formattedDate);
            Log.d("incident time", "" + incDate);
            Date incidentDate = df.parse(incDate);
            Date currentDate2 = df.parse(formattedDate);
            long diff = currentDate2.getTime() - incidentDate.getTime();
            long seconds = TimeUnit.SECONDS.convert(diff, TimeUnit.MILLISECONDS);
            Log.d("seconds", "" + seconds);
            return seconds;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return -1;
    }
}