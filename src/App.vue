<template>
  <div class="w-full min-h-screen bg-white text-black font-space-grotesk overflow-auto">
    <!-- Header -->
    <header class="w-full fixed top-0 z-50 bg-gray-900 shadow-lg border-b-2 border-red-600">
      <nav class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <!-- Logo -->
        <div class="flex items-center gap-2">
          <div class="text-3xl font-bold tracking-tight">
            <span class="text-white">Find</span><span class="text-red-600">My</span><span class="text-white">Car</span>
          </div>
        </div>
        
        <!-- User Actions -->
        <div class="flex items-center gap-4">
          <div v-if="isUserLoggedIn" class="flex items-center gap-3">
            <div class="text-right">
              <div class="text-sm font-semibold text-white">{{ userName }}</div>
              <div class="text-xs text-gray-400">{{ userEmail }}</div>
            </div>
            <div class="w-10 h-10 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-sm border-2 border-white">
              {{ userName ? userName.charAt(0).toUpperCase() : 'U' }}
            </div>
          </div>
          
          <button 
            v-if="!isUserLoggedIn"
            @click="showLoginModal = true"
            class="px-6 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-semibold transition-all shadow-md hover:shadow-lg hover:scale-105"
          >
            Login
          </button>
          <button 
            v-else
            @click="handleLogout"
            class="px-6 py-2.5 bg-white hover:bg-gray-100 text-gray-900 rounded-lg text-sm font-semibold transition-all border-2 border-gray-300 hover:border-white"
          >
            Logout
          </button>
        </div>
      </nav>
    </header>

    <!-- Login Modal -->
    <div 
      v-if="showLoginModal" 
      class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black bg-opacity-90 backdrop-blur-sm"
      @click.self="showLoginModal = false"
    >
      <div class="glass-card rounded-3xl max-w-md w-full p-8 bg-white border border-gray-200 shadow-xl">
        <div class="flex justify-between items-start mb-6">
          <h3 class="text-2xl font-bold text-gray-900">Login / Register</h3>
          <button 
            @click="showLoginModal = false"
            class="text-gray-400 hover:text-white text-2xl"
          >
            ×
          </button>
        </div>
        <Login 
          :isUserLoggedIn="isUserLoggedIn"
          @user-authenticated="handleUserAuthenticated"
        />
      </div>
    </div>

    <!-- Hero Section -->
    <section class="w-full py-6 px-6 pt-32 relative" :style="{ paddingRight: vehicles.length === 0 ? '360px' : '0' }">
      <!-- Main Content -->
      <div class="max-w-7xl mx-auto fade-in">
        <div class="text-center mb-6">
          <h1 class="text-3xl md:text-5xl font-bold mb-2 text-gray-900">
            Find Your Perfect Car
          </h1>
          <p class="text-base text-gray-600">
            Customize your search and get instant matches
          </p>
        </div>

        <!-- Unified Filters and Sorting Card -->
        <div class="mb-6">
          <Filters 
            ref="filtersComponent"
            :filters="filters"
            @update:carType="filters.carType = $event"
            @update:fuelType="filters.fuelType = $event"
            @update:seats="filters.seats = $event"
            @update:budgetMin="filters.budget.min = $event"
            @update:budgetMax="filters.budget.max = $event"
            @update:sizeImportance="filters.sizeImportance = $event"
            @update:powerImportance="filters.powerImportance = $event"
            @update:safetyImportance="filters.safetyImportance = $event"
            @update:popularityImportance="filters.popularityImportance = $event"
            @update:fuelEfficiencyImportance="filters.fuelEfficiencyImportance = $event"
            @update:maintenanceCostImportance="filters.maintenanceCostImportance = $event"
          />
        </div>

        <!-- CTA Buttons -->
        <div class="text-center">
          <div class="flex items-center justify-center gap-4">
            <button 
              @click="resetFilters" 
              class="button-modern bg-gray-500 text-white px-8 py-4 text-lg font-semibold rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all hover:bg-gray-600"
            >
              Reset
            </button>
            <button 
              @click="suggestCars" 
              :disabled="loading"
              class="button-modern bg-red-600 text-white px-16 py-4 text-lg font-semibold rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {{ loading ? 'Loading...' : 'Find Cars' }}
            </button>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="mt-3 text-red-500 text-sm">
            {{ errorMessage }}
          </div>
        </div>
      </div>

      <!-- Horizontal News Window - Right Side -->
      <div v-if="vehicles.length === 0" class="news-window-horizontal">
        <News />
      </div>
    </section>

    <!-- Vehicle Results Section -->
    <section v-if="hasSearched" class="w-full px-6 py-24">
      <div class="max-w-7xl mx-auto">
        <!-- No Vehicles Found Message -->
        <div v-if="vehicles.length === 0" class="text-center py-16">
          <div class="max-w-md mx-auto">
            <svg class="mx-auto h-24 w-24 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">No Vehicles Found</h3>
            <p class="text-gray-600 mb-6">Try adjusting your filters to see more results.</p>
            <button 
              @click="resetFilters" 
              class="button-modern bg-gray-500 text-white px-8 py-3 rounded-full font-semibold hover:bg-gray-600 transition"
            >
              Reset Filters
            </button>
          </div>
        </div>

        <!-- Vehicles Found -->
        <div v-else>
          <div class="flex justify-between items-center mb-16">
            <h2 class="text-5xl font-bold text-gray-900">Found {{ vehicles.length }} Vehicles</h2>
          </div>

          <!-- Vehicle List - Horizontal Bars -->
          <div class="space-y-4">
          <div 
            v-for="(vehicle, index) in paginatedVehicles" 
            :key="index"
            @click="selectVehicle(vehicle)"
            :class="['vehicle-bar glass-card rounded-lg overflow-hidden card-hover cursor-pointer flex items-center gap-6 p-4', { 'ring-2 ring-red-600 bg-red-50': selectedVehicle && selectedVehicle.VehicleName === vehicle.VehicleName }]"
          >
            <!-- Vehicle Image -->
            <div class="flex-shrink-0 w-32 h-24 bg-gradient-to-br from-gray-900 to-gray-800 rounded-lg relative overflow-hidden">
              <img 
                v-if="vehicle['Image URL'] && vehicle['Image URL'].trim()"
                :src="vehicle['Image URL'].trim()"
                :alt="vehicle.VehicleName"
                class="w-full h-full object-cover"
                @error="handleImageError($event)"
              />
              <svg 
                v-else
                class="absolute inset-0 w-full h-full opacity-40" 
                viewBox="0 0 400 300" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M80 150 L110 130 L150 120 L190 120 L230 110 L310 110 L350 120 L380 140 L390 150 L380 160 L350 165 L330 165 L310 160 L130 160 L110 165 L80 165 Z" fill="#D90429" opacity="0.8" />
                <ellipse cx="130" cy="165" rx="18" ry="18" fill="#fff" />
                <ellipse cx="130" cy="165" rx="10" ry="10" fill="#000" />
                <ellipse cx="310" cy="165" rx="18" ry="18" fill="#fff" />
                <ellipse cx="310" cy="165" rx="10" ry="10" fill="#000" />
              </svg>
            </div>

            <!-- Vehicle Info -->
            <div class="flex-1 flex items-center justify-between gap-4">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <span class="minimal-badge">{{ vehicle.BodyType || 'Car' }}</span>
                  <span class="minimal-badge">{{ vehicle.FuelType || 'N/A' }}</span>
                </div>

                <h3 class="text-xl font-bold text-gray-900 mb-1">{{ vehicle.VehicleName }}</h3>
                <p class="text-gray-600 text-sm">{{ vehicle['Brand name'] }}</p>
              </div>

              <div class="flex items-center gap-6">
                <div class="text-right">
                  <div class="text-gray-900 font-bold text-lg">
                    ₹{{ vehicle.PriceCheapestVariant || 'N/A' }} - ₹{{ vehicle.PriceMostExpensiveVariant || 'N/A' }} L
                  </div>
                  <div class="text-gray-500 text-xs mt-1">
                    {{ vehicle.Seats }} Seats
                  </div>
                </div>

                <!-- Link Button -->
                <div 
                  v-if="vehicle.Link && vehicle.Link.trim() && vehicle.Link.trim().startsWith('http')"
                  @click.stop
                  class="flex-shrink-0"
                >
                  <a 
                    :href="vehicle.Link.trim()"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 text-sm font-semibold rounded-full flex items-center gap-2 transition-all duration-300 shadow-md hover:shadow-lg cursor-pointer no-underline"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="flex-shrink-0">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M15 3h6v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span>Visit</span>
                  </a>
                </div>

                <span class="text-red-600 text-sm font-medium hover:underline flex-shrink-0">View Details →</span>
              </div>
            </div>
          </div>
          </div>

          <!-- Pagination Controls -->
          <div v-if="totalPages > 1" class="mt-8 flex items-center justify-center gap-2">
            <button
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <div class="flex gap-2">
              <button
                v-for="page in totalPages"
                :key="page"
                @click="currentPage = page"
                :class="['px-4 py-2 rounded-lg font-semibold transition', currentPage === page ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']"
              >
                {{ page }}
              </button>
            </div>
            
            <button
              @click="currentPage = Math.min(totalPages, currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>

          <!-- Page Info -->
          <div v-if="vehicles.length > 0" class="mt-4 text-center text-gray-600 text-sm">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, vehicles.length) }} of {{ vehicles.length }} vehicles
          </div>
        </div>
      </div>
    </section>

    <!-- Vehicle Details Modal -->
    <div 
      v-if="selectedVehicle" 
      class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black bg-opacity-90 backdrop-blur-sm"
      @click.self="selectedVehicle = null"
    >
      <div class="glass-card rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-y-auto bg-white border border-gray-200 shadow-xl">
        <div class="p-8">
          <div class="flex justify-between items-start mb-6">
            <h3 class="text-4xl font-bold text-gray-900">{{ selectedVehicle.VehicleName }}</h3>
            <button 
              @click="selectedVehicle = null"
              class="text-gray-600 hover:text-gray-900 text-2xl"
            >
              ×
            </button>
          </div>

          <!-- Vehicle Image in Modal -->
          <div v-if="selectedVehicle['Image URL'] && selectedVehicle['Image URL'].trim()" class="mb-6">
            <img 
              :src="selectedVehicle['Image URL'].trim()"
              :alt="selectedVehicle.VehicleName"
              class="w-full h-64 object-cover rounded-lg"
              @error="handleImageError($event)"
            />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="detail-item">
              <span class="label">Brand:</span>
              <span class="value">{{ selectedVehicle['Brand name'] }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Body Type:</span>
              <span class="value">{{ selectedVehicle.BodyType }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Fuel Type:</span>
              <span class="value">{{ selectedVehicle.FuelType }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Seats:</span>
              <span class="value">{{ selectedVehicle.Seats }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Price Range:</span>
              <span class="value">₹{{ selectedVehicle.PriceCheapestVariant }} - ₹{{ selectedVehicle.PriceMostExpensiveVariant }} Lakhs</span>
            </div>
            <div class="detail-item">
              <span class="label">Maintenance Cost:</span>
              <span class="value">₹{{ selectedVehicle.MaintenanceCost }} Lakhs</span>
            </div>
            <div class="detail-item">
              <span class="label">Safety Rating:</span>
              <span class="value">{{ selectedVehicle.SafetyRating }}/5</span>
            </div>
            <div class="detail-item">
              <span class="label">Fuel Efficiency:</span>
              <span class="value">{{ selectedVehicle.FuelEfficiency }} km/l</span>
            </div>
            <div class="detail-item">
              <span class="label">Power:</span>
              <span class="value">{{ selectedVehicle.Power }} bhp</span>
            </div>
            <div class="detail-item">
              <span class="label">Length:</span>
              <span class="value">{{ selectedVehicle.Length }} mm</span>
            </div>
            <div class="detail-item">
              <span class="label">Width:</span>
              <span class="value">{{ selectedVehicle.Width }} mm</span>
            </div>
            <div class="detail-item">
              <span class="label">Height:</span>
              <span class="value">{{ selectedVehicle.Height }} mm</span>
            </div>
            <div class="detail-item">
              <span class="label">Ground Clearance:</span>
              <span class="value">{{ selectedVehicle.GroundClearance }} mm</span>
            </div>
            <div class="detail-item">
              <span class="label">Sales:</span>
              <span class="value">{{ selectedVehicle.Sales }}</span>
            </div>
          </div>

          <!-- Link Button in Modal -->
          <a 
            v-if="selectedVehicle.Link && selectedVehicle.Link.trim()"
            :href="selectedVehicle.Link.trim()"
            target="_blank"
            rel="noopener noreferrer"
            class="mt-6 w-full button-modern bg-red-600 text-white px-6 py-3 rounded-full font-semibold flex items-center justify-center gap-2 hover:bg-red-700 transition"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M15 3h6v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Visit Official Website
          </a>

          <!-- Comments Section -->
          <div class="mt-8 border-t border-gray-200 pt-6">
            <h4 class="text-xl font-bold text-gray-900 mb-4">💬 Comments ({{ vehicleComments.length }})</h4>
            
            <!-- Comment Form (only for logged in users) -->
            <div v-if="isUserLoggedIn" class="mb-6">
              <textarea
                v-model="newComment"
                placeholder="Write your comment..."
                class="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900 bg-white focus:outline-none focus:border-red-600 resize-none"
                rows="3"
              ></textarea>
              <button
                @click="submitComment"
                :disabled="!newComment.trim()"
                class="mt-2 px-6 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Post Comment
              </button>
            </div>
            <div v-else class="mb-4 text-sm text-gray-600">
              <p>Please <button @click="showLoginModal = true" class="text-red-600 hover:underline font-semibold">login</button> to leave a comment.</p>
            </div>

            <!-- Comments List -->
            <div class="space-y-4 max-h-64 overflow-y-auto">
              <div v-if="vehicleComments.length === 0" class="text-gray-500 text-sm py-4">
                No comments yet. Be the first to comment!
              </div>
              <div
                v-for="comment in vehicleComments"
                :key="comment.id"
                class="bg-gray-50 rounded-lg p-4 border border-gray-200"
              >
                <div class="flex items-start justify-between mb-2">
                  <div>
                    <span class="font-semibold text-gray-900">{{ comment.userName }}</span>
                  </div>
                  <button
                    v-if="isUserLoggedIn && comment.userId === userId"
                    @click="deleteComment(comment.id)"
                    class="text-red-600 hover:text-red-800 text-sm font-medium ml-2"
                    title="Delete comment"
                  >
                    Delete
                  </button>
                </div>
                <p class="text-gray-700">{{ comment.comment }}</p>
              </div>
            </div>
          </div>

          <button 
            @click="selectedVehicle = null" 
            class="mt-4 w-full button-modern bg-gray-700 text-white px-6 py-3 rounded-full font-semibold hover:bg-gray-600 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Login from './components/Login.vue';
import Filters from './components/filters.vue';
import News from './components/news.vue';
import { localHost } from './utils/urls';

export default {
  name: "App",
  components: {
    Login,
    Filters,
    News,
  },
  // Computed properties: automatically update when their dependencies change
  // These are like "smart variables" that recalculate when needed
  computed: {
    // Get login status from Vuex store (global state management)
    isUserLoggedIn() {
      return this.$store.state.isUserLoggedIn;
    },
    userEmail() {
      return this.$store.state.userEmail;
    },
    userId() {
      return this.$store.state.userId;
    },
    userName() {
      return this.$store.state.userName;
    },
    // Filter comments to show only those for the currently selected vehicle
    vehicleComments() {
      if (!this.selectedVehicle) return [];
      return this.comments.filter(c => c.vehicleName === this.selectedVehicle.VehicleName);
    },
    // Get only the vehicles for the current page (for pagination)
    paginatedVehicles() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.vehicles.slice(start, end);
    },
    // Calculate total number of pages needed
    totalPages() {
      return Math.ceil(this.vehicles.length / this.itemsPerPage);
    },
  },
  data() {
    return {
      filters: {
        carType: "",
        fuelType: "",
        seats: "",
        budget: { min: 5, max: 30 },
        sizeImportance: 5,
        powerImportance: 5,
        safetyImportance: 5,
        popularityImportance: 5,
        fuelEfficiencyImportance: 5,
        maintenanceCostImportance: 5,
      },
      vehicles: [],
      selectedVehicle: null,
      loading: false,
      errorMessage: '',
      showLoginModal: false,
      comments: [],
      newComment: '',
      hasSearched: false,
      currentPage: 1,
      itemsPerPage: 10,
    };
  },
  // Watchers: run code when specific data changes
  watch: {
    // Ensure budget min doesn't exceed max
    'filters.budget.min'(newVal) {
      if (newVal > this.filters.budget.max) {
        this.filters.budget.min = this.filters.budget.max;
      }
    },
    // Ensure budget max doesn't go below min
    'filters.budget.max'(newVal) {
      if (newVal < this.filters.budget.min) {
        this.filters.budget.max = this.filters.budget.min;
      }
    },
    // Save filters to localStorage whenever they change
    filters: {
      handler(newFilters) {
        this.saveFiltersToSession(newFilters);
      },
      deep: true, // Watch nested properties (like budget.min, budget.max)
    },
    // Load comments when a vehicle is selected
    selectedVehicle() {
      if (this.comments.length === 0) {
        this.fetchComments();
      }
    },
  },
  // Lifecycle hook: runs when component is added to the page
  mounted() {
    this.loadFiltersFromSession();
    this.fetchComments();
  },
  methods: {
    // Main function to fetch and filter vehicles from CSV
    async suggestCars() {
      this.loading = true;
      this.errorMessage = '';
      this.hasSearched = true;
      this.vehicles = [];
      this.currentPage = 1;
      
      try {
        // Add timestamp to URL to prevent browser caching
        const timestamp = new Date().getTime();
        const response = await fetch(`/improved_car_data2.csv?t=${timestamp}`, {
          cache: 'no-cache',
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}. Make sure the dev server is running and the file exists in the public folder.`);
        }
        
        // Read CSV file as text
        const csvText = await response.text();
        
        if (!csvText || csvText.trim().length === 0) {
          throw new Error('CSV file is empty');
        }
        
        // Split CSV into lines and remove empty lines
        const lines = csvText.split('\n').filter(line => line.trim());

        if (lines.length < 2) {
          throw new Error('CSV file is empty or invalid');
        }

        // First line contains column headers (e.g., "VehicleName", "Brand name", etc.)
        const headers = lines[0].split(',').map(h => h.trim());
        const vehicles = [];
        
        // Process each row of data (skip first row which is headers)
        for (let i = 1; i < lines.length; i++) {
          const line = lines[i].trim();
          if (!line) continue;
          
          // Split row into columns
          const columns = line.split(',');
          const vehicle = {};
          
          // Map each column to its header name
          headers.forEach((header, index) => {
            vehicle[header] = index < columns.length ? (columns[index]?.trim() || '') : '';
          });

          // Skip if vehicle doesn't have a name
          if (!vehicle.VehicleName) continue;

          // Check if vehicle matches all selected filters
          let matchesAllFilters = true;

          // Filter 1: Body Type (exact match)
          if (this.filters.carType && vehicle.BodyType !== this.filters.carType) {
            matchesAllFilters = false;
          }

          // Filter 2: Fuel Type (handles partial matches like "Petrol/CNG" matching "Petrol")
          if (matchesAllFilters && this.filters.fuelType) {
            const vehicleFuelType = (vehicle.FuelType || '').toLowerCase();
            const selectedFuelType = this.filters.fuelType.toLowerCase();
            
            // Special handling for Electric/EV (they mean the same thing)
            if (selectedFuelType === 'ev' || selectedFuelType === 'electric') {
              if (!vehicleFuelType.includes('electric') && !vehicleFuelType.includes('ev')) {
                matchesAllFilters = false;
              }
            } else {
              // For other fuel types, check if vehicle's fuel type contains the selected type
              // Example: "Petrol/CNG" contains "Petrol", so it matches
              if (!vehicleFuelType.includes(selectedFuelType)) {
                matchesAllFilters = false;
              }
            }
          }

          // Filter 3: Number of Seats (exact match)
          if (matchesAllFilters && this.filters.seats && vehicle.Seats !== this.filters.seats) {
            matchesAllFilters = false;
          }

          // Filter 4: Budget Range (check if price range overlaps with selected budget)
          if (matchesAllFilters) {
            const vehicleMinPrice = parseFloat(vehicle.PriceCheapestVariant) || 0;
            const vehicleMaxPrice = parseFloat(vehicle.PriceMostExpensiveVariant) || 0;
            const selectedMinBudget = this.filters.budget.min;
            const selectedMaxBudget = this.filters.budget.max;

            // Vehicle matches if its price range overlaps with selected budget
            // Example: Vehicle ₹8-20L matches budget ₹10-30L (overlaps at ₹10-20L)
            if (vehicleMaxPrice < selectedMinBudget || vehicleMinPrice > selectedMaxBudget) {
              matchesAllFilters = false;
            }
          }

          // If vehicle passes all filters, add it to results
          if (matchesAllFilters) {
            vehicles.push(vehicle);
          }
        }
        
        // Sort vehicles by user's preference weights (size, power, safety, etc.)
        if (vehicles.length > 0 && this.$refs.filtersComponent) {
          const sortedVehicles = this.$refs.filtersComponent.sortVehiclesByScore(vehicles);
          this.vehicles = [...sortedVehicles];
        } else {
          this.vehicles = vehicles;
        }
        
        this.selectedVehicle = null;
        
        if (vehicles.length === 0) {
          this.errorMessage = 'No vehicles found matching your criteria.';
        }
      } catch (error) {
        this.errorMessage = `Error: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    selectVehicle(vehicle) {
      this.selectedVehicle = vehicle;
    },
    handleUserAuthenticated() {
      this.showLoginModal = false;
    },
    handleLogout() {
      this.$store.commit('userLoggedOut');
      this.selectedVehicle = null;
      this.vehicles = [];
    },
    // Save user's filter preferences to browser storage (persists across page refreshes)
    saveFiltersToSession(filters) {
      try {
        localStorage.setItem('carFilters', JSON.stringify(filters));
      } catch (error) {
        // Silently fail if localStorage is not available (e.g., private browsing mode)
      }
    },
    
    // Load saved filter preferences when app starts
    loadFiltersFromSession() {
      try {
        const savedFilters = localStorage.getItem('carFilters');
        if (savedFilters) {
          const parsedFilters = JSON.parse(savedFilters);
          // Restore all filter values with defaults if missing
          this.filters = {
            carType: parsedFilters.carType || "",
            fuelType: parsedFilters.fuelType || "",
            seats: parsedFilters.seats || "",
            budget: {
              min: parsedFilters.budget?.min || 5,
              max: parsedFilters.budget?.max || 30,
            },
            sizeImportance: parsedFilters.sizeImportance || 5,
            powerImportance: parsedFilters.powerImportance || 5,
            safetyImportance: parsedFilters.safetyImportance || 5,
            popularityImportance: parsedFilters.popularityImportance || 5,
            fuelEfficiencyImportance: parsedFilters.fuelEfficiencyImportance || 5,
            maintenanceCostImportance: parsedFilters.maintenanceCostImportance || 5,
          };
        }
      } catch (error) {
        // Silently fail if localStorage is not available
      }
    },
    async fetchComments() {
      try {
        const response = await fetch(`${localHost}/comments`);
        if (response.ok) {
          this.comments = await response.json();
        }
      } catch (error) {
        // Silently fail if API is not available
      }
    },
    
    async submitComment() {
      if (!this.newComment.trim() || !this.isUserLoggedIn || !this.selectedVehicle) {
        return;
      }

      try {
        const comment = {
          vehicleName: this.selectedVehicle.VehicleName,
          userId: this.userId,
          userName: this.userName,
          comment: this.newComment.trim(),
        };

        const response = await fetch(`${localHost}/comments`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(comment),
        });

        if (response.ok) {
          this.newComment = '';
          await this.fetchComments();
        } else {
          alert('Failed to post comment. Please try again.');
        }
      } catch (error) {
        alert('Error posting comment. Please try again.');
      }
    },
    
    async deleteComment(commentId) {
      if (!this.isUserLoggedIn) {
        return;
      }

      if (!confirm('Are you sure you want to delete this comment?')) {
        return;
      }

      try {
        const response = await fetch(`${localHost}/comments/${commentId}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          await this.fetchComments();
        } else {
          alert('Failed to delete comment. Please try again.');
        }
      } catch (error) {
        alert('Error deleting comment. Please try again.');
      }
    },
    
    handleImageError(event) {
      event.target.style.display = 'none';
    },
    
    resetFilters() {
      this.filters = {
        carType: "",
        fuelType: "",
        seats: "",
        budget: { min: 5, max: 30 },
        sizeImportance: 5,
        powerImportance: 5,
        safetyImportance: 5,
        popularityImportance: 5,
        fuelEfficiencyImportance: 5,
        maintenanceCostImportance: 5,
      };
      this.vehicles = [];
      this.selectedVehicle = null;
      this.errorMessage = '';
      this.hasSearched = false;
      this.currentPage = 1;
    },
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

body {
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #000;
  color: #fff;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.font-space-grotesk {
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
}

.gradient-text {
  background: linear-gradient(135deg, #fff 0%, #999 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.card-hover {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-hover:hover {
  transform: translateY(-2px);
}

.vehicle-bar {
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.vehicle-bar:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-color: rgba(217, 4, 41, 0.3);
}

.button-modern {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.button-modern::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.button-modern:hover::before {
  left: 100%;
}

.button-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(217, 4, 41, 0.4);
}

.glass-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.filter-pill {
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.2);
  background: rgba(0, 0, 0, 0.05);
}

.filter-pill:hover {
  border-color: #D90429;
  background: rgba(217, 4, 41, 0.1);
  transform: translateY(-2px);
}

.filter-pill.active {
  border-color: #D90429;
  background: #D90429;
  color: white;
}

.minimal-badge {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(217, 4, 41, 0.1);
  border: 1px solid rgba(217, 4, 41, 0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  color: #D90429;
}

.fade-in {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.detail-item .label {
  font-weight: 500;
  color: #9CA3AF;
}

.detail-item .value {
  color: #1f2937;
  font-weight: 600;
}

/* Custom range input styling */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  height: 6px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: #D90429;
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #D90429;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}

select {
  background-color: white;
  color: #1f2937;
}

select option {
  background-color: white;
  color: #1f2937;
}

/* Horizontal News Window Styles - Right Side */
.news-window-horizontal {
  position: fixed;
  top: 80px;
  right: 0;
  width: 360px;
  height: calc(100vh - 80px);
  z-index: 30;
  background: rgba(255, 255, 255, 0.98);
  border-left: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: -4px 0 12px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

@media (max-width: 1024px) {
  .news-window-horizontal {
    width: 320px;
  }
}

@media (max-width: 768px) {
  .news-window-horizontal {
    width: 100%;
    height: 200px;
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
    border-right: none;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
  }
}
</style>
