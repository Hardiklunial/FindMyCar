import axios from 'axios';
import * as cheerio from 'cheerio';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function scrapeCarWaleNews() {
  try {
    console.log('Fetching CarWale news page...');
    
    // Fetch the news page
    const response = await axios.get('https://www.carwale.com/news/', {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });

    const $ = cheerio.load(response.data);
    const newsItems = [];

    // Find all news articles - CarWale uses specific selectors
    // Looking for article links and titles
    $('a').each((index, element) => {
      const $el = $(element);
      const href = $el.attr('href');
      const text = $el.text().trim();
      
      // Look for news article links (they typically contain /news/ in the URL)
      if (href && href.includes('/news/') && text && text.length > 20) {
        // Try to find author and timestamp from parent elements
        const $parent = $el.parent();
        const $article = $el.closest('article, div, li');
        
        // Extract author (usually in format "By AuthorName")
        let author = '';
        $article.find('*').each((i, el) => {
          const text = $(el).text();
          if (text.includes('By ') && text.length < 50) {
            author = text.replace('By ', '').trim();
            return false; // break
          }
        });
        
        // Extract timestamp (usually "X hours/days ago")
        let timestamp = '';
        $article.find('*').each((i, el) => {
          const text = $(el).text();
          if ((text.includes('ago') || text.includes('hour') || text.includes('day')) && text.length < 30) {
            timestamp = text.trim();
            return false; // break
          }
        });

        // Avoid duplicates
        if (!newsItems.find(item => item.title === text || item.url === href)) {
          newsItems.push({
            id: newsItems.length + 1,
            title: text,
            url: href.startsWith('http') ? href : `https://www.carwale.com${href}`,
            author: author || 'CarWale Team',
            timestamp: timestamp || 'Recently',
            scrapedAt: new Date().toISOString()
          });
        }
      }
    });

    // Alternative approach: Look for specific article structures
    // CarWale might use specific class names or structures
    $('h2, h3').each((index, element) => {
      const $el = $(element);
      const title = $el.text().trim();
      const $link = $el.find('a').first();
      const href = $link.attr('href') || $el.parent('a').attr('href');
      
      if (title && title.length > 20 && href && href.includes('/news/')) {
        // Check if we already have this title
        if (!newsItems.find(item => item.title === title)) {
          // Try to find author nearby
          let author = 'CarWale Team';
          let timestamp = 'Recently';
          
          // Look in sibling or parent elements
          const $container = $el.closest('div, article, li');
          $container.find('*').each((i, el) => {
            const text = $(el).text().trim();
            // Check if text contains "By AuthorName X hours ago" format
            if (text.includes('By ') && (text.includes('ago') || text.includes('hour') || text.includes('day'))) {
              // Extract author and timestamp from combined string
              const match = text.match(/By\s+(.+?)\s+(\d+\s+(?:hours?|days?|minutes?)\s+ago)/i);
              if (match) {
                author = match[1].trim();
                timestamp = match[2].trim();
              } else {
                // Fallback: try to separate manually
                const byIndex = text.indexOf('By ');
                if (byIndex !== -1) {
                  const afterBy = text.substring(byIndex + 3);
                  // Try to find where timestamp starts (usually a number)
                  const timeMatch = afterBy.match(/(\d+\s+(?:hours?|days?|minutes?)\s+ago)/i);
                  if (timeMatch) {
                    author = afterBy.substring(0, afterBy.indexOf(timeMatch[0])).trim();
                    timestamp = timeMatch[1].trim();
                  }
                }
              }
            } else if (text.includes('By ') && text.length < 50 && !text.includes('ago')) {
              // Just author without timestamp
              author = text.replace('By ', '').trim();
            } else if ((text.includes('ago') || text.includes('hour') || text.includes('day')) && text.length < 30 && !text.includes('By ')) {
              // Just timestamp without author
              timestamp = text.trim();
            }
          });

          newsItems.push({
            id: newsItems.length + 1,
            title: title,
            url: href.startsWith('http') ? href : `https://www.carwale.com${href}`,
            author: author,
            timestamp: timestamp,
            scrapedAt: new Date().toISOString()
          });
        }
      }
    });

    // Clean up author and timestamp fields
    const cleanedNews = newsItems.map(item => {
      let author = item.author || 'CarWale Team';
      let timestamp = item.timestamp || 'Recently';
      
      // Clean author - remove any timestamp that got attached
      if (author.includes('ago') || author.includes('hour') || author.includes('day')) {
        // Extract just the author name
        const authorMatch = author.match(/^(.+?)(?:\s+\d+\s+(?:hours?|days?|minutes?)\s+ago)/i);
        if (authorMatch) {
          author = authorMatch[1].trim();
        } else {
          // Try to remove timestamp part
          author = author.replace(/\d+\s+(?:hours?|days?|minutes?)\s+ago/i, '').trim();
        }
      }
      
      // Clean timestamp - remove any "By Author" prefix
      if (timestamp.includes('By ')) {
        timestamp = timestamp.replace(/By\s+[^0-9]+/i, '').trim();
      }
      
      // Remove any extra spaces
      author = author.replace(/\s+/g, ' ').trim();
      timestamp = timestamp.replace(/\s+/g, ' ').trim();
      
      return {
        ...item,
        author: author || 'CarWale Team',
        timestamp: timestamp || 'Recently'
      };
    });

    // Remove duplicates and limit to 20 most recent
    const uniqueNews = cleanedNews
      .filter((item, index, self) => 
        index === self.findIndex(t => t.title === item.title)
      )
      .slice(0, 20);

    console.log(`Found ${uniqueNews.length} news articles`);

    // Read existing db.json
    let dbData = { users: [] };
    const dbPath = path.join(__dirname, 'db.json');
    
    if (fs.existsSync(dbPath)) {
      const existingData = fs.readFileSync(dbPath, 'utf8');
      dbData = JSON.parse(existingData);
    }

    // Update with news
    dbData.news = uniqueNews;

    // Write back to db.json
    fs.writeFileSync(dbPath, JSON.stringify(dbData, null, 2));
    console.log('News saved to db.json');

    return uniqueNews;
  } catch (error) {
    console.error('Error scraping news:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data.substring(0, 200));
    }
    throw error;
  }
}

// Run the scraper
scrapeCarWaleNews()
  .then(news => {
    console.log('Scraping completed successfully!');
    console.log(`Total articles: ${news.length}`);
  })
  .catch(error => {
    console.error('Scraping failed:', error);
    process.exit(1);
  });

