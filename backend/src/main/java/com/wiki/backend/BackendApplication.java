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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.security.crypto.bcrypt.BCrypt;

import java.util.List;
import java.util.Optional;

@SpringBootApplication
@RestController
public class BackendApplication {

    @Autowired
    private PageRepository pageRepository;

    @Autowired
    private UserRepository userRepository;

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

    @GetMapping("/user/{email}")
    public ResponseEntity<User> getUser(@PathVariable String email) {
        Optional<User> user = userRepository.findById(email);
        return user.map(ResponseEntity::ok)
                   .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/user")
    public User createUser(@RequestBody User user) {
        return userRepository.save(user);
    }

    @PutMapping("/user/{email}")
    public ResponseEntity<User> updateUser(@PathVariable String email, @RequestBody User userDetails) {
        return userRepository.findById(email)
            .map(user -> {
                user.setName(userDetails.getName());
                user.setPasswordHash(userDetails.getPasswordHash());
                return ResponseEntity.ok(userRepository.save(user));
            })
            .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/user/{email}")
    public ResponseEntity<User> deleteUser(@PathVariable String email) {
        return userRepository.findById(email)
            .map(user -> {
                userRepository.delete(user);
                return ResponseEntity.ok(user);
            })
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/authenticateUser")
    public boolean authenticateUser(@RequestParam String email, @RequestParam String password) {
        Optional<User> userOpt = userRepository.findById(email);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            String storedHash = user.getPasswordHash();
            // Compare the provided password with the stored hash
            return BCrypt.checkpw(password, storedHash);
        }
        return false;
    }
}
