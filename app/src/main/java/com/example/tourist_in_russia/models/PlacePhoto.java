package com.example.tourist_in_russia.models;

import com.google.gson.annotations.SerializedName;

public class PlacePhoto {
    @SerializedName("id")
    private int id;

    @SerializedName("photo_path")
    private String photoPath;

    @SerializedName("place_id")
    private int placeId;

    @SerializedName("created_at")
    private String createdAt;

    // Getters
    public int getId() {
        return id;
    }

    public String getPhotoPath() {
        return photoPath;
    }

    public int getPlaceId() {
        return placeId;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    // Setters
    public void setId(int id) {
        this.id = id;
    }

    public void setPhotoPath(String photoPath) {
        this.photoPath = photoPath;
    }

    public void setPlaceId(int placeId) {
        this.placeId = placeId;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }
} 