package edu.temple.pihomesecuritymobile;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.MediaScannerConnection;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.util.Random;

public class ImageViewer extends AppCompatActivity {
    private final String url_prefix = "https://d1uydrbc3kb9ug.cloudfront.net/";
    private final int STORAGE_REQUEST_CODE = 29;
    private String global_url;

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
        final String url = url_prefix + images[position];
        Log.d("image url", "" + url);
        global_url = url;
        Picasso.get().load(url).into(imageView);
        Button backButton = findViewById(R.id.buttonBack);
        Button uploadButton = findViewById(R.id.buttonSafe);
        Button downloadButton = findViewById(R.id.buttonDownload);

        downloadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //first need to check if we have permission to write to external storage and get permission if we don't have
                if (ContextCompat.checkSelfPermission(ImageViewer.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED ) {
                    ActivityCompat.requestPermissions(ImageViewer.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_REQUEST_CODE);
                } else {
                    new DownloadImage().execute(url);
                }
            }
        });
    }

    private class DownloadImage extends AsyncTask<String, Void, Bitmap> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Toast.makeText(ImageViewer.this, "Downloading image...", Toast.LENGTH_LONG).show();
        }

        @Override
        protected Bitmap doInBackground(String... URL) {
            String imageURL = URL[0];
            Bitmap bitmap = null;
            try {
                // Download Image from URL
                InputStream input = new java.net.URL(imageURL).openStream();
                // Decode Bitmap
                bitmap = BitmapFactory.decodeStream(input);
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(ImageViewer.this, "Error downloading image", Toast.LENGTH_LONG).show();
            }
            return bitmap;
        }
        @Override
        protected void onPostExecute(Bitmap result) {
            Toast.makeText(ImageViewer.this, "Image successfully downloaded", Toast.LENGTH_LONG).show();
            saveImage(result);
        }
    }

    protected void saveImage(Bitmap bitmap) {
        String root = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES).toString();
        File myDir = new File(root + "/saved_images");
        myDir.mkdirs();
        Random generator = new Random();
        int n = 10000;
        n = generator.nextInt(n);
        String fname = "Image-" + n + ".jpg";
        File file = new File(myDir, fname);
        if (file.exists()) {
            file.delete();
        }
        try {
            file.createNewFile();
            FileOutputStream out = new FileOutputStream(file);
            bitmap.compress(Bitmap.CompressFormat.JPEG, 90, out);
            out.flush();
            out.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Tell the media scanner about the new file so that it is
        // immediately available to the user.
        MediaScannerConnection.scanFile(this, new String[]{file.toString()}, null,
                new MediaScannerConnection.OnScanCompletedListener() {
                    public void onScanCompleted(String path, Uri uri) {
                        Log.i("ExternalStorage", "Scanned " + path + ":");
                        Log.i("ExternalStorage", "-> uri=" + uri);
                    }
                });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == STORAGE_REQUEST_CODE) {
            //user said yes to external storage use
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(ImageViewer.this, "External storage permission granted", Toast.LENGTH_LONG).show();
                new DownloadImage().execute(global_url);

            } else {
                //user said no to external storage use
                Toast.makeText(ImageViewer.this, "External storage permission denied", Toast.LENGTH_LONG).show();
            }
        }
    }
}
