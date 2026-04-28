/**
 * Ampoulex ERP - Main JavaScript
 * Common utilities and functionality used across the application
 */

// ============================================================================
// Global Configuration
// ============================================================================

const Ampoulex = {
  config: {
    apiBaseUrl: '/api',
    csrfToken: document.querySelector('meta[name="csrf-token"]')?.content || '',
    debug: false,
    toastTimeout: 5000
  },
  
  // ============================================================================
  // Utility Functions
  // ============================================================================
  
  /**
   * Format currency value
   * @param {number} amount - Amount to format
   * @param {string} currency - Currency code (default: PKR)
   * @returns {string} Formatted currency string
   */
  formatCurrency(amount, currency = 'PKR') {
    return new Intl.NumberFormat('en-PK', {
      style: 'currency',
      currency: currency
    }).format(amount);
  },
  
  /**
   * Format date
   * @param {Date|string} date - Date to format
   * @param {string} format - Format type (short, long, time)
   * @returns {string} Formatted date string
   */
  formatDate(date, format = 'short') {
    const d = new Date(date);
    
    if (isNaN(d.getTime())) {
      return 'Invalid Date';
    }
    
    const options = {
      short: { year: 'numeric', month: '2-digit', day: '2-digit' },
      long: { year: 'numeric', month: 'long', day: 'numeric' },
      time: { hour: '2-digit', minute: '2-digit' },
      datetime: { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit', 
        minute: '2-digit'
      }
    };
    
    return d.toLocaleString('en-PK', options[format] || options.short);
  },
  
  /**
   * Format number with thousands separator
   * @param {number} num - Number to format
   * @returns {string} Formatted number string
   */
  formatNumber(num) {
    return new Intl.NumberFormat('en-PK').format(num);
  },
  
  /**
   * Debounce function
   * @param {Function} func - Function to debounce
   * @param {number} wait - Wait time in milliseconds
   * @returns {Function} Debounced function
   */
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },
  
  /**
   * Throttle function
   * @param {Function} func - Function to throttle
   * @param {number} limit - Time limit in milliseconds
   * @returns {Function} Throttled function
   */
  throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  },
  
  // ============================================================================
  // API Functions
  // ============================================================================
  
  /**
   * Make API request
   * @param {string} url - API endpoint URL
   * @param {Object} options - Fetch options
   * @returns {Promise} Response promise
   */
  async api(url, options = {}) {
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': this.config.csrfToken
      },
      credentials: 'same-origin'
    };
    
    const mergedOptions = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...(options.headers || {})
      }
    };
    
    try {
      const response = await fetch(`${this.config.apiBaseUrl}${url}`, mergedOptions);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: 'Request failed' }));
        throw new Error(error.message || `HTTP ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      this.showToast('error', error.message || 'An error occurred');
      throw error;
    }
  },
  
  /**
   * GET request
   * @param {string} url - Endpoint URL
   * @returns {Promise} Response promise
   */
  get(url) {
    return this.api(url, { method: 'GET' });
  },
  
  /**
   * POST request
   * @param {string} url - Endpoint URL
   * @param {Object} data - Request data
   * @returns {Promise} Response promise
   */
  post(url, data) {
    return this.api(url, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },
  
  /**
   * PUT request
   * @param {string} url - Endpoint URL
   * @param {Object} data - Request data
   * @returns {Promise} Response promise
   */
  put(url, data) {
    return this.api(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  },
  
  /**
   * DELETE request
   * @param {string} url - Endpoint URL
   * @returns {Promise} Response promise
   */
  delete(url) {
    return this.api(url, { method: 'DELETE' });
  },
  
  // ============================================================================
  // UI Functions
  // ============================================================================
  
  /**
   * Show toast notification
   * @param {string} type - Toast type (success, error, warning, info)
   * @param {string} message - Message to display
   * @param {number} timeout - Auto-close timeout (ms)
   */
  showToast(type, message, timeout = null) {
    const toastTimeout = timeout || this.config.toastTimeout;
    
    const icons = {
      success: 'check-circle',
      error: 'exclamation-circle',
      warning: 'exclamation-triangle',
      info: 'info-circle'
    };
    
    const classes = {
      success: 'bg-success',
      error: 'bg-danger',
      warning: 'bg-warning',
      info: 'bg-info'
    };
    
    const toast = `
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header ${classes[type] || 'bg-secondary'} text-white">
          <i class="fas fa-${icons[type] || 'info'} me-2"></i>
          <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
          ${message}
        </div>
      </div>
    `;
    
    const container = document.getElementById('toast-container') || this.createToastContainer();
    container.insertAdjacentHTML('beforeend', toast);
    
    setTimeout(() => {
      const toastElement = container.lastElementChild;
      if (toastElement) {
        toastElement.remove();
      }
    }, toastTimeout);
  },
  
  /**
   * Create toast container if it doesn't exist
   * @returns {HTMLElement} Toast container element
   */
  createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
  },
  
  /**
   * Show confirmation dialog
   * @param {string} message - Confirmation message
   * @returns {Promise<boolean>} User confirmation result
   */
  async confirm(message) {
    return new Promise((resolve) => {
      if (window.Swal) {
        Swal.fire({
          title: 'Are you sure?',
          text: message,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel'
        }).then((result) => {
          resolve(result.isConfirmed);
        });
      } else {
        resolve(confirm(message));
      }
    });
  },
  
  /**
   * Show loading state on button
   * @param {HTMLElement} button - Button element
   * @param {string} loadingText - Loading text
   */
  showLoading(button, loadingText = 'Loading...') {
    if (!button) return;
    
    button.disabled = true;
    button.dataset.originalText = button.innerHTML;
    button.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${loadingText}`;
    button.classList.add('loading');
  },
  
  /**
   * Hide loading state on button
   * @param {HTMLElement} button - Button element
   */
  hideLoading(button) {
    if (!button) return;
    
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || 'Submit';
    button.classList.remove('loading');
    delete button.dataset.originalText;
  },
  
  // ============================================================================
  // Form Functions
  // ============================================================================
  
  /**
   * Serialize form data to object
   * @param {HTMLFormElement} form - Form element
   * @returns {Object} Form data object
   */
  serializeForm(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
      if (data[key]) {
        if (!Array.isArray(data[key])) {
          data[key] = [data[key]];
        }
        data[key].push(value);
      } else {
        data[key] = value;
      }
    }
    
    return data;
  },
  
  /**
   * Validate required fields in form
   * @param {HTMLFormElement} form - Form element
   * @returns {boolean} Validation result
   */
  validateRequired(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
      if (!field.value.trim()) {
        isValid = false;
        field.classList.add('is-invalid');
        
        // Remove invalid class on input
        field.addEventListener('input', function() {
          this.classList.remove('is-invalid');
        }, { once: true });
      } else {
        field.classList.remove('is-invalid');
      }
    });
    
    return isValid;
  },
  
  // ============================================================================
  // Storage Functions
  // ============================================================================
  
  /**
   * Save to localStorage
   * @param {string} key - Storage key
   * @param {*} value - Value to store
   */
  saveToStorage(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Storage error:', error);
    }
  },
  
  /**
   * Get from localStorage
   * @param {string} key - Storage key
   * @returns {*} Stored value or null
   */
  getFromStorage(key) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error('Storage error:', error);
      return null;
    }
  },
  
  /**
   * Remove from localStorage
   * @param {string} key - Storage key
   */
  removeFromStorage(key) {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Storage error:', error);
    }
  }
};

// ============================================================================
// Initialize on DOM Ready
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
  console.log('Ampoulex ERP initialized');
  
  // Add CSRF token to all AJAX requests if using jQuery
  if (window.jQuery) {
    $.ajaxSetup({
      headers: {
        'X-CSRF-Token': Ampoulex.config.csrfToken
      }
    });
  }
  
  // Initialize tooltips
  if (window.bootstrap) {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
  
  // Initialize popovers
  if (window.bootstrap) {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });
  }
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Ampoulex;
}
