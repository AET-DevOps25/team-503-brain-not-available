package com.wiki.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class BackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(BackendApplication.class, args);
	}

	@GetMapping("/page/{pageId}")
	public ResponseEntity<Page> getPage(@PathVariable int pageId) {
		Page page = new Page();
		page.setPageId(pageId);
		page.setTitle("This could be a title!");
		page.setContent("You are looking at page " + pageId + " of the wiki!");
		return ResponseEntity.ok(page);
	}

}
