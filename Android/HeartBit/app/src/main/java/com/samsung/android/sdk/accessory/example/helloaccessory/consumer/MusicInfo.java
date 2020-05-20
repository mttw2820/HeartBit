package com.samsung.android.sdk.accessory.example.helloaccessory.consumer;

public class MusicInfo {
    public int musicNum;        // 음악 번호
    public int searchTagNum;   // 소속 태그 번호
    public String title;        // 음악 제목
    public String singer;       // 가수 이름

    public int getMusicNum() {
        return musicNum;
    }

    public void setMusicNum(int musicNum) {
        this.musicNum = musicNum;
    }

    public int getSearchTagNum() {
        return searchTagNum;
    }

    public void setSearchTagNum(int searchTagNum) {
        this.searchTagNum = searchTagNum;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getSinger() {
        if(singer==null) return "UNKNOWN";
        return singer;
    }

    public void setSinger(String singer) {
        this.singer = singer;
    }
}
