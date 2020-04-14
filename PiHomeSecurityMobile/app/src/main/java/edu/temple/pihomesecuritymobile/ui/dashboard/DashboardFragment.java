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

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

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
    JSONArray dataArr;
    Context parent;
    onFragListener mList;
    String home_ID;
    String current_username;

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
            if(dataObj == null){
                dataArr = rsp.getBodyArray();
                Log.d("JSONArray", dataArr.toString());
            } else {
                Log.d("JSONObject", dataObj.toString());
            }
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
        TextView incID = root.findViewById(R.id.textView2);
        TextView occDate = root.findViewById(R.id.textView3);
        //TextView adminComm = root.findViewById(R.id.textView4);
        GridView gridView = root.findViewById(R.id.gridViewInc);
        int set = -1;

        Button escalateButton = root.findViewById(R.id.escalate);
        escalateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                JSONObject msg = new JSONObject();;
                try{
                    msg.put("message_type","escalate");
                    msg.put("rsp_type",1);
                } catch (Exception e){
                    Log.e("ESC_FAIL",e.toString());
                }
                new AlertDialog.Builder(parent)
                        .setTitle("Confirm Action")
                        .setMessage("You are about to escalate this incident which will contact the authorities. Are you sure you want to continue?")
                        .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                //mList.escalateRsp(msg);
                                mngr.alertResponse(home_ID, "yes");
                                Toast.makeText(parent.getApplicationContext(), "Sending escalation response.", Toast.LENGTH_SHORT).show();
                            }
                        })
                        .setNegativeButton("Cancel", null)
                        .show();
            }
        });

        Button resolveButton = root.findViewById(R.id.resolve);
        resolveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                JSONObject msg = new JSONObject();;
                try{
                    msg.put("message_type","escalate");
                    msg.put("rsp_type",0);
                } catch (Exception e){
                    Log.e("ESC_FAIL",e.toString());
                }
                new AlertDialog.Builder(parent)
                        .setTitle("Confirm Action")
                        .setMessage("You are about to mark this incident as resolved. Are you sure you want to continue?")
                        .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                //mList.resolveRsp(msg);
                                mngr.alertResponse(home_ID, "no");
                                Toast.makeText(parent.getApplicationContext(), "Sending de-escalation response.", Toast.LENGTH_SHORT).show();
                            }
                        })
                        .setNegativeButton("Cancel", null)
                        .show();
            }
        });

        if (dataObj==null && dataArr==null) { //no incidents exist yet
            set = -1;
        } else if(dataObj == null){ //only one incident exists
            set = 0;
        } else if(dataArr == null){ //multiple incidents exist
            set = 1;
        }
        try{
            if (set == -1) {
                incID.setText("No Incident data available.");
                occDate.setText("");
            } else if(set ==1){
                String IDstr = dataObj.getString("IncidentID");
                incID.setText( "Incident ID: " + IDstr);
                Log.d("incidentID", "" + IDstr);
                String incDate = dataObj.getString("DateRecorded");
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
            } else if(set == 0){
                JSONObject tmp = dataArr.getJSONObject(0);
                String IDstr = tmp.getString("IncidentID");
                incID.setText( "Incident ID: " + IDstr);
                Log.d("incidentID", "" + IDstr);
                String incDate = tmp.getString("DateRecorded");
                occDate.setText("Incident occurred at: " + incDate);
                mngr.updateStatement("IncidentData", "LastAccessed", "current_timestamp()", "IncidentID", IDstr);

                if (current_username!=null) {
                    mngr.updateStatement("IncidentData", "UserAccessed", current_username, "IncidentID", IDstr);
                }
                String paths = tmp.getString("ImagePaths");
                Log.d("paths", "" + paths);
                final String[] imagePaths = paths.split(",");
                IncidentImageAdapter incidentImageAdapter = new IncidentImageAdapter(root.getContext(), imagePaths);
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
        void escalateRsp(JSONObject msg);
        void resolveRsp(JSONObject msg);
    }
}