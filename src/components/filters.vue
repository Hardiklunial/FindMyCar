<template>
  <div class="filters-container">
    <!-- Advanced Filters -->
    <div class="max-w-2xl mx-auto mb-8">
      <div class="glass-card rounded-3xl p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Body Type Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Body Type</label>
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
            <label class="block text-sm font-medium text-gray-700 mb-2">Fuel Type</label>
            <select 
              :value="filters.fuelType"
              @change="$emit('update:fuelType', $event.target.value)"
              class="w-full bg-white border border-gray-300 rounded-lg px-4 py-2 text-gray-900 focus:outline-none focus:border-red-600"
            >
              <option value="">All Fuel Types</option>
              <option>Petrol</option>
              <option>Diesel</option>
              <option>Petrol Hybrid</option>
              <option>Diesel Hybrid</option>
              <option>Electric</option>
              <option>EV</option>
              <option>Petrol CNG</option>
              <option>Petrol/CNG</option>
            </select>
          </div>

          <!-- Seats Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Seats</label>
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
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Budget: ₹{{ filters.budget.min }} - ₹{{ filters.budget.max }} Lakhs
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
  emits: ['update:carType', 'update:fuelType', 'update:seats', 'update:budgetMin', 'update:budgetMax'],
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

