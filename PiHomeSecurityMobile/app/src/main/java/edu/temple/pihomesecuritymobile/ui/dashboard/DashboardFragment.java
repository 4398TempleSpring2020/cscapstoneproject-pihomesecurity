package edu.temple.pihomesecuritymobile.ui.dashboard;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import edu.temple.pihomesecuritymobile.ContentManager;
import edu.temple.pihomesecuritymobile.R;
import edu.temple.pihomesecuritymobile.models.Request;
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

        if(HomeID.equals("")){
            errMess = "HomeID was not found";
        } else {
            String result = mngr.getIncidents(HomeID);
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
        View root = inflater.inflate(R.layout.fragment_dashboard, container, false);
        final TextView textView = root.findViewById(R.id.text_dashboard);
        textView.setText("Incidents");
        TextView incID = root.findViewById(R.id.textView2);
        TextView occDate = root.findViewById(R.id.textView3);
        TextView adminComm = root.findViewById(R.id.textView4);
        int set = -1;
        if(dataObj == null){
            set = 0;
        } else if(dataArr == null){
            set = 1;
        }
        try{
            if(set ==1){
                String IDstr = "Incident ID: "+ dataObj.getInt("IncidentID");
                incID.setText(IDstr);
                occDate.setText("Incident occurred at: "+dataObj.getString("DateRecorded"));
                adminComm.setText("Admin Comments:\n"+dataObj.getString("AdminComments"));
            } else if(set == 0){
                JSONObject tmp = dataArr.getJSONObject(0);
                String IDstr = "Incident ID: "+ tmp.getInt("IncidentID");
                incID.setText(IDstr);
                occDate.setText("Incident occurred at: "+tmp.getString("DateRecorded"));
                adminComm.setText("Admin Comments:\n"+tmp.getString("AdminComments"));
            }

        } catch(JSONException e){
            incID.setText(errMess);
            occDate.setText("");
            adminComm.setText("");
        }
        return root;
    }

    @Override
    public void onDetach(){
        super.onDetach();
        mList = null;
    }

    public interface onFragListener{

    }
}