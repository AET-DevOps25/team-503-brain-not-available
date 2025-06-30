package com.wiki.backend;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.TestPropertySource;
import org.springframework.http.*;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(locations = "classpath:application-test.properties")
class BackendApplicationTests {

	@LocalServerPort
	private int port;

	@Autowired
	private TestRestTemplate restTemplate;

	private String getBaseUrl() {
		return "http://localhost:" + port;
	}

	@Test
	public void testPageObject() {
		// Given
		Page page = new Page();
		String title = "Some title";
		String content = "Some content";
		int id = 42;

		// When
		page.setTitle(title);
		page.setContent(content);
		page.setPageId(id);

		// Then
		assertEquals(title, page.getTitle());
		assertEquals(content, page.getContent());
		assertEquals(id, page.getPageId());
	}

	@Test
	void testCreatePage() {
		// Given
		Page page = new Page();
		page.setTitle("Test Page");
		page.setContent("This is a test page.");

		// When
		ResponseEntity<Page> response = restTemplate.postForEntity(getBaseUrl() + "/page", page, Page.class);

		// Then
		assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
		assertThat(response.getBody()).isNotNull();
		assertThat(response.getBody().getPageId()).isNotNull();
		assertThat(response.getBody().getTitle()).isEqualTo("Test Page");
		assertThat(response.getBody().getContent()).isEqualTo("This is a test page.");
	}

	@Test
	void testGetAllPages() {
		ResponseEntity<Page[]> response = restTemplate.getForEntity(getBaseUrl() + "/pages", Page[].class);

		assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
		assertThat(response.getBody()).isNotNull();
	}

	@Test
	void testGetPageById_NotFound() {
		ResponseEntity<Page> response = restTemplate.getForEntity(getBaseUrl() + "/page/99999", Page.class);
		assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
	}

	@Test
	void testUpdatePage() {
		// Original page
		Page page = new Page();
		page.setTitle("Original Title");
		page.setContent("Original Content");
		Page createdPage = restTemplate.postForEntity(getBaseUrl() + "/page", page, Page.class).getBody();
		assertThat(createdPage != null).isTrue();

		// Update page
        createdPage.setTitle("Updated Title");
		createdPage.setContent("Updated Content");

		HttpEntity<Page> requestEntity = new HttpEntity<>(createdPage);
		ResponseEntity<Page> response = restTemplate.exchange(
				getBaseUrl() + "/page/" + createdPage.getPageId(),
				HttpMethod.PUT,
				requestEntity,
				Page.class
		);

		assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
		assertThat(response.getBody()).isNotNull();
		assertThat(response.getBody().getTitle()).isEqualTo("Updated Title");
	}

	@Test
	void testDeletePage() {
		// Original page
		Page page = new Page();
		page.setTitle("To Be Deleted");
		page.setContent("Temporary Content");
		Page createdPage = restTemplate.postForEntity(getBaseUrl() + "/page", page, Page.class).getBody();
		assertThat(createdPage != null).isTrue();

		// Delete page
		ResponseEntity<Page> response = restTemplate.exchange(
				getBaseUrl() + "/page/" + createdPage.getPageId(),
				HttpMethod.DELETE,
				null,
				Page.class
		);

		assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
		assertThat(response.getBody()).isNotNull();
		assertThat(response.getBody().getPageId()).isEqualTo(createdPage.getPageId());

		// Confirm deletion
		ResponseEntity<Page> check = restTemplate.getForEntity(getBaseUrl() + "/page/" + createdPage.getPageId(), Page.class);
		assertThat(check.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
	}
}
