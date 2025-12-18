<template>
  <div class="filters-container">
    <!-- Unified Card with Filters and Sorting -->
    <div class="glass-card rounded-2xl p-6 shadow-lg">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Filters Section -->
        <div>
          <h3 class="text-lg font-bold text-gray-900 mb-4 pb-2 border-b border-gray-200">Filters</h3>
          <div class="space-y-3">
            <!-- Body Type Filter -->
            <div>
              <label class="block text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Body Type</label>
              <select 
                :value="filters.carType"
                @change="$emit('update:carType', $event.target.value)"
                class="w-full bg-white border border-gray-300 rounded-lg px-4 py-2 text-gray-900 focus:outline-none focus:border-red-600"
              >
                <option value="">All Types</option>
                <option>Sedan</option>
                <option>Hatchback</option>
                <option>SUV</option>
                <option>MPV</option>
                <option>Compact SUV</option>
              </select>
            </div>

            <!-- Fuel Type Filter -->
            <div>
              <label class="block text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Fuel Type</label>
              <select 
                :value="filters.fuelType"
                @change="$emit('update:fuelType', $event.target.value)"
                class="w-full bg-white border border-gray-300 rounded-lg px-4 py-2 text-gray-900 focus:outline-none focus:border-red-600"
              >
                <option value="">All Fuel Types</option>
                <option>Petrol</option>
                <option>Diesel</option>
                <option>Hybrid</option>
                <option>Electric</option>
                <option>EV</option>
                <option>CNG</option>
                <option>Petrol CNG</option>
                <option>Petrol/CNG</option>
              </select>
            </div>

            <!-- Seats Filter -->
            <div>
              <label class="block text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Seats</label>
              <select 
                :value="filters.seats"
                @change="$emit('update:seats', $event.target.value)"
                class="w-full bg-white border border-gray-300 rounded-lg px-4 py-2 text-gray-900 focus:outline-none focus:border-red-600"
              >
                <option value="">Any</option>
                <option>2</option>
                <option>4</option>
                <option>5</option>
                <option>6-7</option>
              </select>
            </div>

            <!-- Budget Filter -->
            <div>
              <label class="block text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">
                Budget: ₹{{ filters.budget.min }} - ₹{{ filters.budget.max }}L
              </label>
              <div class="flex gap-2">
                <div class="flex-1">
                  <label class="text-xs text-gray-500 mb-1 block">Min: ₹{{ filters.budget.min }}L</label>
                  <input 
                    type="range" 
                    :min="1" 
                    :max="filters.budget.max" 
                    :value="filters.budget.min"
                    @input="$emit('update:budgetMin', parseInt($event.target.value))"
                    class="w-full"
                  />
                </div>
                <div class="flex-1">
                  <label class="text-xs text-gray-500 mb-1 block">Max: ₹{{ filters.budget.max }}L</label>
                  <input 
                    type="range" 
                    :min="filters.budget.min" 
                    :max="500" 
                    :value="filters.budget.max"
                    @input="$emit('update:budgetMax', parseInt($event.target.value))"
                    class="w-full"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sorting Preferences Section -->
        <div>
          <h3 class="text-lg font-bold text-gray-900 mb-4 pb-2 border-b border-gray-200">Sorting Preferences</h3>
          <p class="text-xs text-gray-500 mb-4">Rate importance (1-10)</p>
          
          <div class="space-y-3">
            <!-- Vehicle Size Importance -->
            <div>
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Vehicle Size</label>
                <span class="text-sm font-bold text-red-600">{{ filters.sizeImportance || 5 }}/10</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="10" 
                :value="filters.sizeImportance || 5"
                @input="$emit('update:sizeImportance', parseInt($event.target.value))"
                class="w-full"
              />
            </div>

            <!-- Power Importance -->
            <div>
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Power</label>
                <span class="text-sm font-bold text-red-600">{{ filters.powerImportance || 5 }}/10</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="10" 
                :value="filters.powerImportance || 5"
                @input="$emit('update:powerImportance', parseInt($event.target.value))"
                class="w-full"
              />
            </div>

            <!-- Safety Rating Importance -->
            <div>
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Safety Rating</label>
                <span class="text-sm font-bold text-red-600">{{ filters.safetyImportance || 5 }}/10</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="10" 
                :value="filters.safetyImportance || 5"
                @input="$emit('update:safetyImportance', parseInt($event.target.value))"
                class="w-full"
              />
            </div>

            <!-- Popularity Importance -->
            <div>
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Popularity</label>
                <span class="text-sm font-bold text-red-600">{{ filters.popularityImportance || 5 }}/10</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="10" 
                :value="filters.popularityImportance || 5"
                @input="$emit('update:popularityImportance', parseInt($event.target.value))"
                class="w-full"
              />
            </div>

            <!-- Fuel Efficiency Importance -->
            <div>
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Fuel Efficiency</label>
                <span class="text-sm font-bold text-red-600">{{ filters.fuelEfficiencyImportance || 5 }}/10</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="10" 
                :value="filters.fuelEfficiencyImportance || 5"
                @input="$emit('update:fuelEfficiencyImportance', parseInt($event.target.value))"
                class="w-full"
              />
            </div>

            <!-- Maintenance Cost Importance -->
            <div>
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Maintenance Cost</label>
                <span class="text-sm font-bold text-red-600">{{ filters.maintenanceCostImportance || 5 }}/10</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="10" 
                :value="filters.maintenanceCostImportance || 5"
                @input="$emit('update:maintenanceCostImportance', parseInt($event.target.value))"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Filters',
  props: {
    filters: {
      type: Object,
      required: true,
      default: () => ({
        carType: '',
        fuelType: '',
        seats: '',
        budget: {
          min: 5,
          max: 30,
        },
      }),
    },
  },
  emits: ['update:carType', 'update:fuelType', 'update:seats', 'update:budgetMin', 'update:budgetMax', 'update:sizeImportance', 'update:powerImportance', 'update:safetyImportance', 'update:popularityImportance', 'update:fuelEfficiencyImportance', 'update:maintenanceCostImportance'],
  methods: {
    // Sort vehicles by weighted score based on user preferences
    // This calculates a score for each vehicle and sorts them from best to worst match
    sortVehiclesByScore(vehicles) {
      // Step 1: Calculate vehicle size (volume = length × width × height) for each vehicle
      const vehicleSizes = new Map();
      vehicles.forEach((vehicle, index) => {
        const length = parseFloat(vehicle.Length) || 0;
        const width = parseFloat(vehicle.Width) || 0;
        const height = parseFloat(vehicle.Height) || 0;
        vehicleSizes.set(index, length * width * height);
      });

      // Step 2: Find maximum values for normalization (to compare vehicles fairly)
      let maxSize = 0;
      let maxPower = 0;
      let maxSafety = 0;
      let maxSales = 0;
      let maxEfficiency = 0;

      vehicles.forEach((vehicle, index) => {
        const size = vehicleSizes.get(index);
        if (size > maxSize) maxSize = size;
        if (parseFloat(vehicle.Power) > maxPower) maxPower = parseFloat(vehicle.Power) || 0;
        if (parseFloat(vehicle.SafetyRating) > maxSafety) maxSafety = parseFloat(vehicle.SafetyRating) || 0;
        if (parseFloat(vehicle.Sales) > maxSales) maxSales = parseFloat(vehicle.Sales) || 0;
        const efficiency = parseFloat(vehicle.FuelEfficiency) || 0;
        if (efficiency > maxEfficiency) maxEfficiency = efficiency;
      });

      // Step 3: Calculate score for each vehicle
      const vehicleScores = [];
      vehicles.forEach((vehicle, index) => {
        const size = vehicleSizes.get(index);
        
        // Normalize each metric to 0-10 scale (0 = worst, 10 = best)
        const sizeScore = maxSize > 0 ? (size / maxSize) * 10 : 0;
        const powerScore = maxPower > 0 ? ((parseFloat(vehicle.Power) || 0) / maxPower) * 10 : 0;
        const safetyScore = maxSafety > 0 ? ((parseFloat(vehicle.SafetyRating) || 0) / maxSafety) * 10 : 0;
        const popularityScore = maxSales > 0 ? ((parseFloat(vehicle.Sales) || 0) / maxSales) * 10 : 0;
        const efficiencyScore = maxEfficiency > 0 ? ((parseFloat(vehicle.FuelEfficiency) || 0) / maxEfficiency) * 10 : 0;

        // Maintenance cost: A = cheapest (10), B = medium (5), C = expensive (1)
        const maintenance = (vehicle.MaintenanceCost || '').toUpperCase().trim();
        let maintenanceScore = 0;
        if (maintenance === 'A') maintenanceScore = 10;
        else if (maintenance === 'B') maintenanceScore = 5;
        else if (maintenance === 'C') maintenanceScore = 1;

        // Step 4: Calculate total score by multiplying each metric by its importance weight
        // Higher importance = that metric has more impact on the final score
        const totalScore = 
          (sizeScore * this.filters.sizeImportance) +
          (powerScore * this.filters.powerImportance) +
          (safetyScore * this.filters.safetyImportance) +
          (popularityScore * this.filters.popularityImportance) +
          (efficiencyScore * this.filters.fuelEfficiencyImportance) +
          (maintenanceScore * this.filters.maintenanceCostImportance);

        vehicleScores.push({ index, totalScore });
      });

      // Step 5: Sort by total score (highest first = best match)
      vehicleScores.sort((a, b) => (b.totalScore || 0) - (a.totalScore || 0));
      
      // Step 6: Return vehicles in sorted order
      return vehicleScores.map(item => {
        const originalVehicle = vehicles[item.index];
        // Create new object to avoid Vue reactivity issues
        const newVehicle = {};
        Object.keys(originalVehicle).forEach(key => {
          newVehicle[key] = originalVehicle[key];
        });
        return newVehicle;
      });
    },
  },
};
</script>

<style scoped>
.filters-container {
  width: 100%;
}

.glass-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Range input styling */
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
</style>

