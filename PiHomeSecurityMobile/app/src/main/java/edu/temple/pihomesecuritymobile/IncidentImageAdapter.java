package edu.temple.pihomesecuritymobile;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.squareup.picasso.Picasso;


public class IncidentImageAdapter extends BaseAdapter {
    private Context c;
    private String[] images;
    private final String url_prefix = "https://d1uydrbc3kb9ug.cloudfront.net/";
    public IncidentImageAdapter(@NonNull Context context, @NonNull String[] paths) {
        this.c=context;
        this.images=paths;
    }


    public int getCount() {
        return images.length;
    }

    public String getItem(int position) {
        return null;
    }

    public long getItemId(int position) {
        return 0;
    }

    // create a new ImageView for each item referenced by the Adapter
    public View getView(int position, View convertView, ViewGroup parent) {
        ImageView imageView;

        if (convertView == null) {
            imageView = new ImageView(c);
            imageView.setLayoutParams(new GridView.LayoutParams(200, 120));
            imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
            imageView.setPadding(2, 2, 2, 2);
        } else {
            imageView = (ImageView) convertView;
        }
        String url = url_prefix + images[position];
        Log.d("image url", "" + url);

        Picasso.get().load(url).into(imageView);
        return imageView;
    }
}
