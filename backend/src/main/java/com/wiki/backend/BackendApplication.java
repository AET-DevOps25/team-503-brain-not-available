package com.wiki.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.CrossOrigin;

import java.util.List;
import java.util.Optional;

@SpringBootApplication
@CrossOrigin(origins = "http://localhost:5173")
@RestController
public class BackendApplication {

    @Autowired
    private PageRepository pageRepository;

    public static void main(String[] args) {
        SpringApplication.run(BackendApplication.class, args);
    }

    @GetMapping("/page/{pageId}")
    public ResponseEntity<Page> getPage(@PathVariable int pageId) {
        Optional<Page> page = pageRepository.findById(pageId);
        return page.map(ResponseEntity::ok)
                   .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/pages")
    public List<Page> getAllPages() {
        return pageRepository.findAll();
    }

    @PostMapping("/page")
    public Page createPage(@RequestBody Page page) {
        return pageRepository.save(page);
    }

    @PutMapping("/page/{pageId}")
    public ResponseEntity<Page> updatePage(@PathVariable int pageId, @RequestBody Page pageDetails) {
        return pageRepository.findById(pageId)
            .map(page -> {
                page.setTitle(pageDetails.getTitle());
                page.setContent(pageDetails.getContent());
                return ResponseEntity.ok(pageRepository.save(page));
            })
            .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/page/{pageId}")
    public ResponseEntity<Page> deletePage(@PathVariable int pageId) {
        return pageRepository.findById(pageId)
            .map(page -> {
                pageRepository.delete(page);
                return ResponseEntity.ok(page);
            })
            .orElse(ResponseEntity.notFound().build());
    }
}
