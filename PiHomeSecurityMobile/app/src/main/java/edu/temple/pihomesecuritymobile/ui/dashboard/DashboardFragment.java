package edu.temple.pihomesecuritymobile.ui.dashboard;

import android.content.Context;
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

import org.json.JSONObject;

import edu.temple.pihomesecuritymobile.ContentManager;
import edu.temple.pihomesecuritymobile.R;
import edu.temple.pihomesecuritymobile.models.Request;
import edu.temple.pihomesecuritymobile.models.Response;

public class DashboardFragment extends Fragment {

    private DashboardViewModel dashboardViewModel;


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
        mngr = new ContentManager();
        int incidentID = 0;
        // Place API code to get data to display
        String result = mngr.selectIDStatement("IncidentData","DateRecorded, BadIncidentFlag, AdminComments","IncidentID","'"+incidentID+"'");
        rsp = mngr.makeResponse(result);
        if(rsp.getStatusCode()==mngr.records_not_exist){
            Log.e("DATA", "onAttach: Pulled data Failure");
        } else {
            data = rsp.getBody();
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