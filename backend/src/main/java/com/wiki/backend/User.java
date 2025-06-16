package com.wiki.backend;

import jakarta.persistence.*;

@Entity
public class User {
    @Id
    private String email;

    private String name;
    private String passwordHash;

    // Getters and setters
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getPasswordHash() { return passwordHash; }
    public void setPasswordHash(String passwordHash) { this.passwordHash = passwordHash; }
}