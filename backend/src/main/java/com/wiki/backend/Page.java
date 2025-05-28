package com.wiki.backend;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Page {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer pageId;
    private String title;
    private String content;

    // Getters and setters
    public Integer getPageId() { return pageId; }
    public void setPageId(Integer pageId) { this.pageId = pageId; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
}