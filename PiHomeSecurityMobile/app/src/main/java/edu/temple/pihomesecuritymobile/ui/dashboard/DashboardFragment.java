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
    JSONObject data;
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
            rsp = mngr.makeResponse(result);
        }

        if(rsp.getStatusCode()==mngr.records_not_exist){
            errMess = "Records do not exist";
        } else {
            data = rsp.getBody();
            Log.d("JSONObject", data.toString());
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
        try{

            String IDstr = "Incident ID: "+ data.getInt("incidentID");
            incID.setText(IDstr);
            occDate.setText("Incident occurred at: "+data.getString("dateRecorded"));
            adminComm.setText("Admin Comments:\n"+data.getString("adminComments"));
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