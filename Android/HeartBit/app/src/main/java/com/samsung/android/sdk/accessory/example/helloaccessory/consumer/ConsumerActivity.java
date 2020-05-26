/*
 * Copyright (c) 2015 Samsung Electronics Co., Ltd. All rights reserved. 
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided that 
 * the following conditions are met:
 * 
 *     * Redistributions of source code must retain the above copyright notice, 
 *       this list of conditions and the following disclaimer. 
 *     * Redistributions in binary form must reproduce the above copyright notice, 
 *       this list of conditions and the following disclaimer in the documentation and/or 
 *       other materials provided with the distribution. 
 *     * Neither the name of Samsung Electronics Co., Ltd. nor the names of its contributors may be used to endorse or 
 *       promote products derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 * PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

package com.samsung.android.sdk.accessory.example.helloaccessory.consumer;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.annotation.SuppressLint;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.ImageButton;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ImageView;


public class ConsumerActivity extends Activity {

    private static final String TAG = "onPostExecute(JSONObject result)";
    private static final String YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query=";
    // UI 변수
    private TextView time_message;              // 날씨 시간
    private TextView temp_message;              // 온도
    private TextView weather_message;           // 날씨 정보
    private ImageView weatherImage;             // 날씨 이미지
    private ListView mMessageListView;          // 통신 결과 리스트
    private static ImageView connectedImage;    // 워치 연결 상태
    private static TextView HRMview;            // 최근 심박수 정보
    private ListView mMusicListView;            // 추천 음악 목록
    private ListView mWeatherMusicListView;     // 날씨 기반 추천 음악 목록
    private TextView bpmRecText;
    private TextView weatherRecText;
    //private static TextView mTextView;          // 연결 상태

    // 날씨 변수
    public String time;
    public String temperature;          // 체감 온도
    public static String weather;
    public static double bpm;           // 심박 정보 : -1이면 없음
    public ArrayList<MusicInfo> bpm_musics;
    public ArrayList<MusicInfo> weather_musics;
    // 워치 통신 연결 및 결과 변수
    private static MessageAdapter mMessageAdapter;
    private static MusicAdapter mMusicAdapter;
    private static WeatherMusicAdapter mWeatherMusicAdapter;

    private boolean mIsBound = false;
    private ConsumerService mConsumerService = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        time_message = (TextView) findViewById(R.id.time_message);
        temp_message = (TextView) findViewById(R.id.temp_message);
        weatherImage = (ImageView) findViewById(R.id.weatherImage);
        connectedImage = (ImageView) findViewById(R.id.HRMisConnect);
        HRMview = (TextView) findViewById(R.id.recentHRM);
        bpmRecText = (TextView) findViewById(R.id.bpmRecText);
        weatherRecText = (TextView) findViewById(R.id.weatherRecText);

        mMessageListView = (ListView) findViewById(R.id.lvMessage);
        mMessageAdapter = new MessageAdapter();
        mMessageListView.setAdapter(mMessageAdapter);
        // 음악 정보를 가져오는 변수들
        mMusicListView = (ListView) findViewById(R.id.bpm_musicList);
        mMusicAdapter = new MusicAdapter(this, bpm_musics);
        mMusicListView.setAdapter(mMusicAdapter);
        mWeatherMusicListView = (ListView) findViewById(R.id.weather_musicList);
        mWeatherMusicAdapter = new WeatherMusicAdapter(this, weather_musics);
        mWeatherMusicListView.setAdapter(mWeatherMusicAdapter);
        //mTextView = (TextView) findViewById(R.id.tvStatus);

        // 날씨 정보 가져오기
        getWeatherData();
        bpm = -1;

        // Bind service
        mIsBound = bindService(new Intent(ConsumerActivity.this, ConsumerService.class), mConnection, Context.BIND_AUTO_CREATE);
    }

    @Override
    protected void onDestroy() {
        // Clean up connections
        if (mIsBound == true && mConsumerService != null) {
            if (mConsumerService.closeConnection() == false) {
                //updateTextView("Disconnected");
                updateImageView("off");         // 연결 이미지 수정
                updateHRMdata("NO"); // 심박 정보 수정
                mMessageAdapter.clear();
            }
        }
        // Un-bind service
        if (mIsBound) {
            unbindService(mConnection);
            mIsBound = false;
        }
        super.onDestroy();
    }

    public void mOnClick(View v) {
        switch (v.getId()) {
            // connect 버튼에 두 가지 기능 모두 넣기
            case R.id.buttonConnect: {
                if (mIsBound == true && mConsumerService != null) {
                    mConsumerService.findPeers();
                }
                break;
            }
            case R.id.buttonDisconnect: {
                if (mIsBound == true && mConsumerService != null) {
                    if (mConsumerService.closeConnection() == false) {
                        //updateTextView("Disconnected");
                        updateImageView("off"); // 연결 이미지 수정
                        updateHRMdata("NO"); // 심박 정보 수정
                        Toast.makeText(getApplicationContext(), R.string.ConnectionAlreadyDisconnected, Toast.LENGTH_LONG).show();
                        mMessageAdapter.clear();
                    }
                }
                break;
            }
            case R.id.buttonSend: {
                if (mIsBound == true && mConsumerService != null) {
                    if (mConsumerService.sendData("Hello Accessory!")) {
                    } else {
                        Toast.makeText(getApplicationContext(), R.string.ConnectionAlreadyDisconnected, Toast.LENGTH_LONG).show();
                    }
                }
                // 음악 추천 리스트 받아오기
                updateMusicList();
                Toast.makeText(getApplicationContext(), "MUSIC LIST UPDATE", Toast.LENGTH_LONG).show();
                break;
            }
            default:
        }
    }

    // 초기 연결 확인 과정 + 이미지 설정
    private final ServiceConnection mConnection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName className, IBinder service) {
            mConsumerService = ((ConsumerService.LocalBinder) service).getService();
            //updateTextView("onServiceConnected");
            updateImageView("on"); // 연결 이미지 수정
        }

        @Override
        public void onServiceDisconnected(ComponentName className) {
            mConsumerService = null;
            mIsBound = false;
            //updateTextView("onServiceDisconnected");
            updateImageView("off"); // 연결 이미지 수정
            updateHRMdata("NO"); // 심박 정보 수정
        }
    };

    // 연결 상태 이미지 업데이트
    public static void updateImageView(final String str) {
        if(str == "on")
            connectedImage.setImageResource(R.drawable.ui_hrm_on);
        else if(str=="off")
            connectedImage.setImageResource(R.drawable.ui_hrm_off);
    }

    // 가장 최근 HRM data 가져오기
    public static void updateHRMdata(final String str){
        if(str.length()>=10){
            HRMview.setText(" ... ");
            bpm = -1;
        }
        else if(str.equals("NO")){
            HRMview.setText("NO");
            bpm = -1;
        }
        else {
            HRMview.setText(str);
            bpm = Double.parseDouble(str);
        }
    }

    // 추천 문구 업데이트
    public void updateRecommendText(int bpm_g, int weather_g, int time_g){
        String bpm_recText = "";
        String weather_recText = "";
        ReadDB readPhraseDB = null;

        // DB 연결
        try {
            readPhraseDB = new ReadDB(this);
        } catch (IOException e) {
            e.printStackTrace();
        }
        if(bpm_g == -1){
            bpm_recText = "심박수를 통한 추천";
        } else {
            bpm_recText = readPhraseDB.getRecPhrase(bpm_g, 0);
        }

        if(Math.random()+0.5 < 1){
            weather_recText = readPhraseDB.getRecPhrase(weather_g, 1);
        } else {
            weather_recText = readPhraseDB.getRecPhrase(time_g, 2);
        }


        bpmRecText.setText(bpm_recText);
        weatherRecText.setText(weather_recText);
        return;
    }

    // 추천 음악 리스트 가져오기
    public void updateMusicList(){
        if(temperature == null || time == null){
            Toast.makeText(getApplicationContext(), "Trouble getting weather/time information.", Toast.LENGTH_LONG).show();
            return;
        }
        // DB
        int bpm_group = -1;
        // 추천 알고리즘 - 1. 심박수
        if(bpm == -1){  // 심박 정보가 없는 경우
            bpm_group = -1;
        } else {        // 심박 정보가 있는 경우우
            if(bpm < 100) // 평소 심박
                bpm_group = 2;
            else if(bpm < 140) //중강도 운동
                bpm_group = 0;
            else bpm_group = 3;
        }
        // 추천 알고리즘 -2. 날씨와 시간
        int weather_group[] = {0, 0, 0, 0, 0};
        int weather_g = 0, time_g = 0;
        int i=0;
        for(i=0; i<temperature.length(); i++){
            if(temperature.substring(i,i+1).equals(".")) break;
        }
        int temper = Integer.parseInt(temperature.substring(0, i));
        int hour = Integer.parseInt(time.substring(11, 13));

        // 날씨 & 시간에 따른 그룹 배정
        if(weather.equals("clear")) {
            if (temper >= 15) { weather_group[3]++; weather_g = 3; }
            else { weather_group[0]++; weather_g = 0; }
        } else {
            weather_group[4]++;
            weather_g = 4;
        }
        if(hour>=5 && hour<12) { weather_group[2]++; time_g = 2; }
        else if(hour>=12 && hour<20) { weather_group[3]++; time_g = 3; }
        else { weather_group[1]++; time_g = 1; }

        // DB 접속
        ReadDB readMusicDB = null;
        try {
            readMusicDB = new ReadDB(this);
        } catch (IOException e) {
            e.printStackTrace();
        }

        // 추천 음악 리스트로 받기
        if(bpm_group != -1)
            bpm_musics = readMusicDB.recommendBPMMusic(bpm_group);
        weather_musics = readMusicDB.recommendWeatherMusic(bpm_group, weather_group);

        // 음악 추천 문구 업데이트
        updateRecommendText(bpm_group, weather_g, time_g);

        mMusicAdapter.updateItem(bpm_musics);
        mWeatherMusicAdapter.updateItem(weather_musics);
    }



    // 음악 추천 어댑터
    public class MusicAdapter extends BaseAdapter {
        private Context context;
        private ArrayList<MusicInfo> musiclist;
        LayoutInflater mLayoutInflator = null;

        public MusicAdapter(Context context, ArrayList<MusicInfo> musiclist) {
            this.context = context;
            this.musiclist = musiclist;
            mLayoutInflator = LayoutInflater.from(this.context);
        }

        @Override
        public int getCount(){ return (musiclist != null)? musiclist.size() : 0; }
        @Override
        public Object getItem(int i){ return (musiclist!=null && (0<=i && i<musiclist.size()))? musiclist.get(i) : null; }
        @Override
        public long getItemId(int i){ return (musiclist!=null &&(0<=i && i<musiclist.size()))? i : 0; }

        public void updateItem(ArrayList<MusicInfo> updateMusic){
            this.musiclist = updateMusic;
            notifyDataSetChanged();
        }
        @Override
        public View getView(int pos, View convertView, ViewGroup parent) {
            View view = mLayoutInflator.inflate(R.layout.bpm_musiclist, null);

            // 뷰에 컴포넌트 연결
            TextView bpmMusicData = (TextView)view.findViewById(R.id.bpm_musicData);
            MusicInfo music = musiclist.get(pos);
            String bpmMusicDataString = ""+music.getTitle() + "\n- " + music.getSinger();
            bpmMusicData.setText(bpmMusicDataString);

            final String search_key = music.getTitle();
            ImageButton youtube_btn = (ImageButton)view.findViewById(R.id.bMusicYoutube);
            youtube_btn.setOnClickListener(new View.OnClickListener(){
                public void onClick(View v){
                    Intent youtubeIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(YOUTUBE_SEARCH_URL + search_key));
                    startActivity(youtubeIntent);
                }
            });
            return view;
        }
    }

    public class WeatherMusicAdapter extends BaseAdapter {
        private Context context;
        private ArrayList<MusicInfo> musiclist;
        LayoutInflater mLayoutInflator = null;

        public WeatherMusicAdapter(Context context, ArrayList<MusicInfo> musiclist) {
            this.context = context;
            this.musiclist = musiclist;
            mLayoutInflator = LayoutInflater.from(this.context);
        }

        @Override
        public int getCount(){ return (musiclist != null)? musiclist.size() : 0; }
        @Override
        public Object getItem(int i){ return (musiclist!=null && (0<=i && i<musiclist.size()))? musiclist.get(i) : null; }
        @Override
        public long getItemId(int i){ return (musiclist!=null &&(0<=i && i<musiclist.size()))? i : 0; }

        public void updateItem(ArrayList<MusicInfo> updateMusic){
            this.musiclist = updateMusic;
            notifyDataSetChanged();
        }
        @Override
        public View getView(int pos, View convertView, ViewGroup parent) {
            View view = mLayoutInflator.inflate(R.layout.weather_musiclist, null);

            // 뷰에 컴포넌트 연결
            TextView bpmMusicData = (TextView)view.findViewById(R.id.weather_musicData);
            MusicInfo music = musiclist.get(pos);
            String bpmMusicDataString = music.getTitle() + "\n- " + music.getSinger();
            bpmMusicData.setText(bpmMusicDataString);

            final String search_key = music.getTitle();
            ImageButton youtube_btn = (ImageButton)view.findViewById(R.id.wMusicYoutube);
            youtube_btn.setOnClickListener(new View.OnClickListener(){
                public void onClick(View v){
                    Intent youtubeIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(YOUTUBE_SEARCH_URL + search_key));
                    startActivity(youtubeIntent);
                }
            });

            return view;
        }
    }

    // OpenWeatherMap API 날씨 데이터 가져오기
    public void getWeatherData(){
        String url = "http://api.openweathermap.org/data/2.5/forecast?id=1835848&APPID=e15fd013b9546defed30a9e0e7444fba&units=metric";
        ReceiveWeatherTask receiveUseTask = new ReceiveWeatherTask();
        receiveUseTask.execute(url);
    }

    public class ReceiveWeatherTask extends AsyncTask<String, Void, JSONObject>{
        protected void onPreExecute(){ super.onPreExecute(); }
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
            } catch (Exception e){
                e.printStackTrace();
            }
            return null;
        }

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




    // 워치와 주고받는 메세지 어뎁터
    public static void addMessage(String data) {
        mMessageAdapter.addMessage(new Message(data));
    }

    private class MessageAdapter extends BaseAdapter {
        private static final int MAX_MESSAGES_TO_DISPLAY = 20;
        private List<Message> mMessages;

        public MessageAdapter() {
            mMessages = Collections.synchronizedList(new ArrayList<Message>());
        }

        void addMessage(final Message msg) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if (mMessages.size() == MAX_MESSAGES_TO_DISPLAY) {
                        mMessages.remove(0);
                        mMessages.add(msg);
                    } else {
                        mMessages.add(msg);
                    }
                    notifyDataSetChanged();
                    mMessageListView.setSelection(getCount() - 1);
                }
            });
        }

        void clear() {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    updateHRMdata("NO");
                    mMessages.clear();
                    notifyDataSetChanged();
                }
            });
        }

        @Override
        public int getCount() {
            return mMessages.size();
        }

        @Override
        public Object getItem(int position) {
            return mMessages.get(position);
        }

        @Override
        public long getItemId(int position) {
            return 0;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            LayoutInflater inflator = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            View messageRecordView = null;
            if (inflator != null) {
                messageRecordView = inflator.inflate(R.layout.message, null);
                TextView tvData = (TextView) messageRecordView.findViewById(R.id.tvData);
                Message message = (Message) getItem(position);
                tvData.setText(message.data);
            }
            return messageRecordView;
        }
    }

    private static final class Message {
        String data;

        public Message(String data) {
            super();
            this.data = data;
        }
    }
}
