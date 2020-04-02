package edu.temple.pihomesecuritymobile;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;

import com.squareup.picasso.Picasso;

public class ImageViewer extends AppCompatActivity {
    private final String url_prefix = "https://d1uydrbc3kb9ug.cloudfront.net/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_viewer);

        // Get intent data
        Intent i = getIntent();

        // Selected image id
        int position = i.getExtras().getInt("image_id");
        String[] images = i.getExtras().getStringArray("images");
        ImageView imageView = findViewById(R.id.ImageViewFull);
        String url = url_prefix + images[position];
        Log.d("image url", "" + url);

        Picasso.get().load(url).into(imageView);
        Button backButton = findViewById(R.id.buttonBack);
        Button uploadButton = findViewById(R.id.buttonSafe);
        Button downloadButton = findViewById(R.id.buttonDownload);
    }
}
