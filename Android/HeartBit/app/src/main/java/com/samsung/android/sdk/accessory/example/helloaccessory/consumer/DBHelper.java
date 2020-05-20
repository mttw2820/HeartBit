package com.samsung.android.sdk.accessory.example.helloaccessory.consumer;

import android.content.Context;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class DBHelper extends SQLiteOpenHelper {
    public static final int DATABASE_VERSION = 1;
    public static String TAG = "DBHelper";
    public static String DB_PATH = "";
    public static String DB_NAME = "MelonMusicDatabase.db";
    private SQLiteDatabase mDataBase;
    private final Context mContext;

    public DBHelper(Context context) {
        super(context, DB_NAME, null, DATABASE_VERSION);
        // DB 위치 조정
        if(android.os.Build.VERSION.SDK_INT >= 17){
            DB_PATH = context.getApplicationInfo().dataDir + "/databases/";
        }
        else{
            DB_PATH = "/data/data/" + context.getPackageName() + "/databases/";
        }
        this.mContext = context;
    }

    public void createDataBase() throws IOException, SQLException, RuntimeException {
        boolean mDataBaseExist = checkDataBase();
        if(!mDataBaseExist){
            try{
                Log.e(TAG,"Before Reading");
                this.getReadableDatabase();
                Log.e(TAG, "After Reading, Before Close");
                this.close();
                copyDataBase();
                Log.e(TAG, "create Database database created");
            }
            catch(Exception e) {
                throw new Error("ERROR COPYING DATABASE");
            }
        }
    }

    // DB를 열어서 쿼리를 쓸 수 있도록 한다.
    public boolean openDataBase() throws SQLException {
        String mPath = DB_PATH + DB_NAME;
        mDataBase = SQLiteDatabase.openDatabase(mPath, null, SQLiteDatabase.CREATE_IF_NECESSARY);
        return mDataBase != null;
    }

    // 경로상 데이터 베이스가 잘 저장되서 읽을 수 있는지 확인
    private boolean checkDataBase(){
        File dbFile = new File(DB_PATH + DB_NAME);
        return dbFile.exists();
    }

    // assets 폴더에서 DB 복사
    private void copyDataBase() throws IOException{
        InputStream mInput = mContext.getAssets().open(DB_NAME);
        String outFileName = DB_PATH + DB_NAME;
        OutputStream mOutput = new FileOutputStream(outFileName);
        byte[] mBuffer = new byte[1024];
        int mLength;
        while((mLength = mInput.read(mBuffer))>0){
            mOutput.write(mBuffer, 0, mLength);
        }
        mOutput.flush();
        mOutput.close();
        mInput.close();
    }

    // DB 종료
    public synchronized void close(){
        if(mDataBase != null)
            mDataBase.close();
        super.close();
    }


    public void onCreate(SQLiteDatabase db){
        // 정보를 추가 저장하는 일도 없을 예정
    }

    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion){
        // 정보 수정 시 -> 사용 안할 예정
    }
}
