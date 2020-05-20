package com.samsung.android.sdk.accessory.example.helloaccessory.consumer;

import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.TextView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Vector;

public class ReadDB {
    protected static final String TAG_TABLE = "TagData";
    protected static final String MUSIC_TABLE = "MusicData";
    protected static final String PHASE_TABLE = "RecommendPhrase";
    private DBHelper helper;
    private SQLiteDatabase mDB;

    public ReadDB(Context context) throws IOException {
        // DB 접속
        try {
            helper = new DBHelper(context);
            helper.createDataBase();
            helper.openDataBase();
        }
        catch(IOException exp){
            throw new Error("NEW ERROR THROUGH READDB");
        }
    }

    public String GetrecommendPhrase(int group, int isBPM){
        String rec_phrase = "";
        rec_phrase = getRecPhrase(group, isBPM);

        return rec_phrase;
    }

    public ArrayList<MusicInfo> recommendBPMMusic(int bpm_group){
        ArrayList<MusicInfo> musicarr;
        Vector<Integer> groups = new Vector<Integer>();     // 가져올 그룹 목록
        Vector<Integer> tags = new Vector<Integer>();       // 가져올 태그 목록

        int music_limit = 3;
        groups.add(bpm_group);
        // group 목록으로 tag리스트 가져오기
        tags = getTags(groups);
        // tag 목록으로 music리스트 가져오기
        musicarr = getMusics(tags, music_limit);

        return musicarr;
    }

    public ArrayList<MusicInfo> recommendWeatherMusic(int bpm_group, int[] weather_group){
        ArrayList<MusicInfo> musicarr;
        Vector<Integer> groups = new Vector<Integer>();     // 가져올 그룹 목록
        Vector<Integer> tags = new Vector<Integer>();       // 가져올 태그 목록

        int music_limit = 0;
        // if bpm group exist -> get 3 tags/group, 2 musics/tag
        if(bpm_group != -1) music_limit = 2;
        else music_limit = 3;

        for(int i=0;i<5;i++){
            if(weather_group[i]!=0)
                groups.add(i);
        }
        // group 목록으로 tag리스트 가져오기
        tags = getTags(groups);
        // tag 목록으로 music리스트 가져오기
        musicarr = getMusics(tags, music_limit);

        return musicarr;
    }

    public ArrayList<MusicInfo> recommendMusic(int bpm_group, int[] weather_group){
        ArrayList<MusicInfo> musicarr;
        Vector<Integer> groups = new Vector<Integer>();     // 가져올 그룹 목록
        Vector<Integer> tags = new Vector<Integer>();       // 가져올 태그 목록

        int music_limit = 0;
        // if bpm group exist -> get 3 tags/group, 2 musics/tag
        if(bpm_group != -1) {
            music_limit = 2;
            groups.add(bpm_group);
        }
        else{
            music_limit = 3;
        }
        for(int i=0;i<5;i++){
            if(weather_group[i]!=0)
                groups.add(i);
        }

        // group 목록으로 tag리스트 가져오기
        tags = getTags(groups);
        // tag 목록으로 music리스트 가져오기
        musicarr = getMusics(tags, music_limit);

        return musicarr;
    }

    protected Vector<Integer> getTags(Vector<Integer> groups){
        try {
            Vector<Integer> dbtags = new Vector<>();
            mDB = helper.getReadableDatabase();

            // 그룹에 해당하는 태그 가져오기
            for(int i=0; i<groups.size(); i++) {
                Integer GROUP = groups.get(i);
                String sql = "SELECT * FROM " + TAG_TABLE + " WHERE groupNum = " + GROUP + " ORDER BY RANDOM() LIMIT 3";
                Cursor cursor = mDB.rawQuery(sql, null);
                int tagcount = cursor.getCount();

                while (cursor.moveToNext()) {
                    // random tag number에 있는 태그 정보 가져오기
                    dbtags.add(cursor.getInt(1));

                }
            }
            return dbtags;
        }
        catch(SQLException mSQLException) {
            Log.e("ReadDBActivity", "getTagData >> catch SQL Exceptions");
            throw mSQLException;
        }
    }

    protected ArrayList<MusicInfo> getMusics(Vector<Integer> tags, int limit){
        try {
            ArrayList<MusicInfo> musics = new ArrayList<>();
            mDB = helper.getReadableDatabase();

            for(int k=0; k<tags.size(); k++) {
                int tagnum = tags.get(k);
                String sql = "SELECT * FROM " + MUSIC_TABLE + " WHERE searchTag = " + tagnum + " ORDER BY RANDOM() LIMIT "+limit;
                Cursor cursor = mDB.rawQuery(sql, null);
                int count = cursor.getCount();

                MusicInfo musicinfo = null;
                while (cursor.moveToNext()) {
                    musicinfo = new MusicInfo();
                    musicinfo.setMusicNum(cursor.getInt(0));
                    musicinfo.setSearchTagNum(tagnum);
                    musicinfo.setTitle(cursor.getString(2));
                    musicinfo.setSinger(cursor.getString(3));

                    musics.add(musicinfo);
                }
            }
            return musics;
        }
        catch(SQLException mSQLException) {
            Log.e("ReadDBActivity", "getMusicData >> catch SQL Exceptions");
            throw mSQLException;
        }
    }

    protected String getRecPhrase(int groupnumber, int isBPM){
        try {
            String phrase = "";
            mDB = helper.getReadableDatabase();

            // 그룹에 해당하는 문구 가져오기
            String sql = "SELECT Phrase FROM " + PHASE_TABLE + " WHERE groupNum = " + groupnumber + " AND IsBPM = " + isBPM + " ORDER BY RANDOM() LIMIT 1";
            Cursor cursor = mDB.rawQuery(sql, null);
            while(cursor.moveToNext()){
                phrase = cursor.getString(0);
            }

            return phrase;
        }
        catch(SQLException mSQLException) {
            Log.e("ReadDBActivity", "getRecommendPhrase >> catch SQL Exceptions");
            throw mSQLException;
        }
    }


    // 랜덤 음악 정보 전달
    public String getInfo(){
        // 정보 가져오기
        TagInfo tag = getTagData();
        MusicInfo music = getMusicData(tag.tagNum);

        // 가져온 정보 올리기
        String info = "Group: "+tag.getGroupNum() + " / Tag Name: "+tag.getTagName() + " // [MUSIC] "+music.getTitle()+" - " +music.getSinger();
        return info;
    }



    protected TagInfo getTagData(){
        try {
            mDB = helper.getReadableDatabase();
            String sql = "SELECT * FROM " + TAG_TABLE;
            Cursor cursor = mDB.rawQuery(sql, null);
            int tagcount = cursor.getCount();
            int randomTagNumber = (int) (Math.random() * tagcount);

            TagInfo taginfo = null;
            if (cursor != null) {
                // random tag number에 있는 태그 정보 가져오기
                for(int i=0;i<randomTagNumber;i++)
                    cursor.moveToNext();

                taginfo = new TagInfo();
                taginfo.setGroupNum(cursor.getInt(0));
                taginfo.setTagNum(cursor.getInt(1));
                taginfo.setTagName(cursor.getString(2));
            }
            return taginfo;
        }
        catch(SQLException mSQLException) {
            Log.e("ReadDBActivity", "getTagData >> catch SQL Exceptions");
            throw mSQLException;
        }
    }

    protected MusicInfo getMusicData(int tagnum){
        try {
            mDB = helper.getReadableDatabase();
            String sql = "SELECT * FROM " + MUSIC_TABLE + " WHERE searchTag = " + tagnum;
            Cursor cursor = mDB.rawQuery(sql, null);
            int count = cursor.getCount();
            int randomMusicNumber = (int) (Math.random() * count);

            MusicInfo musicinfo = null;
            if (cursor != null) {
                for(int i=0;i<randomMusicNumber;i++)
                    cursor.moveToNext();

                musicinfo = new MusicInfo();
                musicinfo.setMusicNum(cursor.getInt(0));
                musicinfo.setSearchTagNum(tagnum);
                musicinfo.setTitle(cursor.getString(2));
                musicinfo.setSinger(cursor.getString(3));
            }
            return musicinfo;
        }
        catch(SQLException mSQLException) {
            Log.e("ReadDBActivity", "getMusicData >> catch SQL Exceptions");
            throw mSQLException;
        }
    }

    // 종료
    public void close(){
        helper.close();
    }
}
