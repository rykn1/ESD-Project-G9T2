new Vue({
    el: '#app',
    data: {
      items: [
        { id: 1, name: 'Item 1', price: 10, quantity: 1 },
        { id: 2, name: 'Item 2', price: 20, quantity: 1 },
        { id: 3, name: 'Item 3', price: 15, quantity: 1 },
        { id: 4, name: 'Item 4', price: 25, quantity: 1 },
        { id: 5, name: 'Item 5', price: 30, quantity: 1 },
        { id: 6, name: 'Item 6', price: 12, quantity: 1 },
        { id: 7, name: 'Item 7', price: 18, quantity: 1 },
        { id: 8, name: 'Item 8', price: 22, quantity: 1 }
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