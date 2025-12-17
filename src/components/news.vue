<template>
  <div class="news-container">
    <div class="news-header">
      <h3 class="news-title">Latest Car News</h3>
    </div>
    
    <div v-if="loading" class="news-loading">
      Loading news...
    </div>
    
    <div v-else-if="error" class="news-error">
      {{ error }}
    </div>
    
    <div v-else-if="news.length === 0" class="news-empty">
      No news available. Run <code>npm run scrape-news</code> to fetch news.
    </div>
    
    <!-- News Display - Shows 6 items, changes every 20 seconds -->
    <div v-else class="news-ticker-container">
      <div 
        v-for="(item, index) in currentNewsItems" 
        :key="`${item.id}-${currentIndex}-${index}`"
        class="news-item"
        @click="openNews(item.url)"
      >
        <div class="news-headline">{{ item.title }}</div>
        <div class="news-bottom">by {{ cleanAuthor(item.author) }} {{ cleanTimestamp(item.timestamp) }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { localHost } from '../utils/urls.js';

export default {
  name: 'News',
  data() {
    return {
      news: [],
      loading: true,
      error: null,
      currentIndex: 0,
      newsInterval: null,
    };
  },
  computed: {
    currentNewsItems() {
      if (this.news.length === 0) return [];
      const itemsPerPage = 6;
      const startIndex = this.currentIndex;
      const items = [];
      
      // Get 6 items starting from currentIndex, wrapping around if needed
      for (let i = 0; i < itemsPerPage; i++) {
        const index = (startIndex + i) % this.news.length;
        items.push(this.news[index]);
      }
      
      return items;
    },
  },
  mounted() {
    this.fetchNews();
  },
  beforeUnmount() {
    // Clean up interval when component is destroyed
    if (this.newsInterval) {
      clearInterval(this.newsInterval);
    }
  },
  methods: {
    async fetchNews() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch(`${localHost}/news`);
        if (!response.ok) {
          throw new Error('Failed to fetch news');
        }
        const data = await response.json();
        this.news = Array.isArray(data) ? data : [];
      } catch (error) {
        console.error('Error fetching news:', error);
        this.error = 'Unable to load news. Make sure json-server is running.';
        // Fallback: try to load from db.json directly
        try {
          const response = await fetch('/db.json');
          const db = await response.json();
          this.news = db.news || [];
          this.error = null;
        } catch (e) {
          this.error = 'News not available. Run: npm run scrape-news';
        }
      } finally {
        this.loading = false;
        // Start the news rotation timer
        if (this.news.length > 0) {
          this.startNewsRotation();
        }
      }
    },
    startNewsRotation() {
      // Clear any existing interval
      if (this.newsInterval) {
        clearInterval(this.newsInterval);
      }
      
      // Change news every 20 seconds (20000 milliseconds)
      // Move by 6 items at a time
      this.newsInterval = setInterval(() => {
        this.currentIndex = (this.currentIndex + 6) % this.news.length;
      }, 20000);
    },
    openNews(url) {
      if (url) {
        window.open(url, '_blank', 'noopener,noreferrer');
      }
    },
    cleanAuthor(author) {
      if (!author) return 'CarWale Team';
      // Remove any timestamp that might be attached
      return author.replace(/\d+\s+(?:hours?|days?|minutes?)\s+ago/gi, '').trim() || 'CarWale Team';
    },
    cleanTimestamp(timestamp) {
      if (!timestamp) return 'Recently';
      // Remove any "By Author" prefix
      return timestamp.replace(/By\s+[^0-9]+/gi, '').trim() || 'Recently';
    },
  },
};
</script>

<style scoped>
.news-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: rgba(255, 255, 255, 0.98);
}

.news-header {
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid rgba(217, 4, 41, 0.2);
}

.news-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.news-loading,
.news-error,
.news-empty {
  padding: 20px;
  text-align: center;
  color: #6b7280;
  font-size: 14px;
}

.news-error {
  color: #dc2626;
}

.news-empty code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
}

.news-ticker-container {
  flex: 1;
  overflow-y: auto;
  position: relative;
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.news-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.02);
  border-left: 3px solid #D90429;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 100px;
  width: 100%;
  animation: fadeIn 0.5s ease-in;
  flex-shrink: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.news-item:hover {
  background: rgba(217, 4, 41, 0.05);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.news-headline {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.5;
  margin: 4px 0;
}

.news-bottom {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

</style>

