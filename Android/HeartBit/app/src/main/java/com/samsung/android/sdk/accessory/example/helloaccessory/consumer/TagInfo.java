package com.samsung.android.sdk.accessory.example.helloaccessory.consumer;

public class TagInfo {
    public int tagNum;      // 태그 번호
    public int groupNum;    // 태그 소속 그룹 번호
    public String tagName;   // 태그 이름

    public int getTagNum() {
        return tagNum;
    }

    public void setTagNum(int tagNum) {
        this.tagNum = tagNum;
    }

    public int getGroupNum() {
        return groupNum;
    }

    public void setGroupNum(int groupNum) {
        this.groupNum = groupNum;
    }

    public String getTagName() {
        return tagName;
    }

    public void setTagName(String tagName) {
        this.tagName = tagName;
    }
}
