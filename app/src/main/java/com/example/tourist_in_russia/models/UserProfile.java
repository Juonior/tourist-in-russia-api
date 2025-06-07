package com.example.tourist_in_russia.models;

import com.google.gson.annotations.SerializedName;

public class UserProfile {
    @SerializedName("id")
    private int id;

    @SerializedName("email")
    private String email;

    @SerializedName("username")
    private String username;

    @SerializedName("is_admin")
    private boolean isAdmin;

    @SerializedName("avatar_path")
    private String avatarPath;

    @SerializedName("created_at")
    private String createdAt;

    // Getters
    public int getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public String getUsername() {
        return username;
    }

    public boolean isAdmin() {
        return isAdmin;
    }

    public String getAvatarPath() {
        return avatarPath;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    // Setters
    public void setId(int id) {
        this.id = id;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setAdmin(boolean admin) {
        isAdmin = admin;
    }

    public void setAvatarPath(String avatarPath) {
        this.avatarPath = avatarPath;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }
} 