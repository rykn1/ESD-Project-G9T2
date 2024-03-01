new Vue({
    el: '#app',
    data: {
      items: [
        { id: 1, name: 'Travel Insurance Bronze', price: 82, quantity: 1 },
        { id: 2, name: 'Neck Pillow', price: 14.99, quantity: 1 },
        { id: 3, name: 'SQ One Way to Tokyo', price: 399, quantity: 1 },
        { id: 4, name: 'ANA One Way to Tokyo', price: 402, quantity: 1 },
        { id: 5, name: 'Ground Tour Seoul', price: 43.42, quantity: 1 },
        { id: 6, name: 'Great Wall of China Pass', price: 15, quantity: 1 },
        { id: 7, name: 'E-Sim Unlimited Wifi 10 Days', price: 23, quantity: 1 },
        { id: 8, name: 'Travel Wifi Router 7 Days', price: 30, quantity: 1 }
      ],
      cart: []
    },
    methods: {
      addItemToCart(item) {
        // Check if item already exists in cart
        const existingItem = this.cart.find(cartItem => cartItem.id === item.id);
        if (existingItem) {
          existingItem.quantity += parseInt(item.quantity);
        } else {
          this.cart.push({...item});
        }
        // Reset quantity to 1
        item.quantity = 1;
      },
      removeItem(index) {
        this.cart.splice(index, 1);
      },
      getTotalPrice() {
        return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
      }
    }
  });