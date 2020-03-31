package com.example.heartbit;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "onPostExecute(JSONObject result)" ;

    //날씨 관련 변수들
    TextView time_message;                 //날씨 시간 정보
    TextView temp_message;              //온도에 대한 메시지
    TextView weather_message;           //날씨 정보에 대한 메시지
    ImageView weatherImage;
    String time;
    String temperature;
    //String feel_temperature;
    static String weather;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        time_message = (TextView) findViewById(R.id.time_message);
        temp_message = (TextView) findViewById(R.id.temp_message);
        //feelTemp_message = (TextView) findViewById(R.id.feelTemp_message);
        //weather_message = (TextView) findViewById(R.id.weather_message);
        weatherImage = (ImageView)findViewById(R.id.weatherImage);
        // 날씨 가져오는 함수
        getWeatherData();

    }
    public void getWeatherData(){
        // API 키 값. 이 url에서 정보 가져옴
        String url = "http://api.openweathermap.org/data/2.5/forecast?id=1835848&APPID=e15fd013b9546defed30a9e0e7444fba&units=metric";
        ReceiveWeatherTask receiveUseTask = new ReceiveWeatherTask();
        receiveUseTask.execute(url);
    }

    // url 연결 위해 필요한 함수 1
    public class ReceiveWeatherTask extends AsyncTask<String, Void, JSONObject>{
        @Override
        protected void onPreExecute(){
            super.onPreExecute();
        }
        @Override
        protected JSONObject doInBackground(String... datas){
            try{
                HttpURLConnection conn = (HttpURLConnection)new URL(datas[0]).openConnection();
                conn.setConnectTimeout(10000);
                conn.setReadTimeout(10000);
                conn.connect();
                if (conn.getResponseCode() == HttpURLConnection.HTTP_OK){
                    InputStream is = conn.getInputStream();
                    InputStreamReader reader = new InputStreamReader(is);
                    BufferedReader in = new BufferedReader(reader);

                    String readed;
                    while ((readed = in.readLine()) != null) {
                        JSONObject jObject = new JSONObject(readed);
                        System.out.println("text = " + jObject);
                        return jObject;
                    }
                }else{
                    return null;
                }
                return null;
            }catch (Exception e){
                e.printStackTrace();
            }
            return null;
        }
        // url 연결 위해 필요한 함수 2
        @SuppressLint("LongLogTag")
        @Override
        protected void onPostExecute(JSONObject result){
            //Log.i(TAG, result.toString());
            if (result != null) {

                try {
                    // 날씨 시간 정보 변수 time
                    time = result.getJSONArray("list").getJSONObject(2).getString("dt_txt");
                    // 온도 변수 temperature
                    temperature = result.getJSONArray("list").getJSONObject(2).getJSONObject("main").getString("temp");
                    // 체감 기온 변수 feel_temperature (사용 안 할 듯)
                    //feel_temperature = result.getJSONArray("list").getJSONObject(2).getJSONObject("main").getString("feels_like");
                    // 날씨 정보 변수 weather
                    weather = result.getJSONArray("list").getJSONObject(2).getJSONArray("weather").getJSONObject(0).getString("main");
                    weather=weather.toLowerCase();
                    time_message.setText(time+"경 의 날씨");
                    temp_message.setText("현재 기온: "+ temperature);
                    //weather_message.setText("날씨: "+weather);

                    // 날씨에 맞는 이미지 갖고오는 함수
                    SetImageToLoad(weather);
                }catch(JSONException e){
                    // 날씨 정보 못 가져올 경우 이곳으로 이동
                    time_message.setText("날씨 정보를 가져오는 중에 문제가 발생했습니다.");
                    e.printStackTrace();
                }
            }

        }

    }

    public void SetImageToLoad(String weatherName) {
        if (weatherName.equals("clear")) {
            weatherImage.setImageResource(R.drawable.sunny);
        }
        else if (weatherName.equals("clouds")){
            weatherImage.setImageResource(R.drawable.cloud);
        }
        else if (weatherName.equals("rain")){
            weatherImage.setImageResource(R.drawable.rain);
        }
        else{

        }
    }

}

