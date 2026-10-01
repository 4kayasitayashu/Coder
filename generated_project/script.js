// Calculator logic script
// Import DOM elements
const display = document.getElementById('display');
const buttons = document.querySelectorAll('.btn');

// State variables
let currentInput = '';
let previousValue = null;
let operator = null;

// Helper to update display
function updateDisplay(value) {
  display.value = value;
}

// Clear all state
function clearAll() {
  currentInput = '';
  previousValue = null;
  operator = null;
  updateDisplay('');
}

// Perform calculation
function compute() {
  const curr = parseFloat(currentInput);
  if (previousValue === null || operator === null || isNaN(curr)) {
    return;
  }
  let result;
  switch (operator) {
    case '+':
      result = previousValue + curr;
      break;
    case '-':
      result = previousValue - curr;
      break;
    case '*':
      result = previousValue * curr;
      break;
    case '/':
      if (curr === 0) {
        result = 'Error';
      } else {
        result = previousValue / curr;
      }
      break;
    default:
      return;
  }
  // Prepare for next operation
  previousValue = typeof result === 'number' ? result : null;
  operator = null;
  currentInput = typeof result === 'number' ? String(result) : '';
  updateDisplay(String(result));
}

// Handle button press
function handleButton(value) {
  if (value >= '0' && value <= '9') {
    // Prevent leading zeros like "00"
    if (currentInput === '0') {
      currentInput = value;
    } else {
      currentInput += value;
    }
    updateDisplay(currentInput);
  } else if (value === '.') {
    if (!currentInput.includes('.')) {
      currentInput = currentInput === '' ? '0.' : currentInput + '.';
      updateDisplay(currentInput);
    }
  } else if (value === 'C') {
    clearAll();
  } else if (value === '=') {
    compute();
  } else if (['+', '-', '*', '/'].includes(value)) {
    // If there is already a pending operation, compute first
    if (operator && currentInput !== '') {
      compute();
    }
    // Store operator and previous value
    previousValue = currentInput !== '' ? parseFloat(currentInput) : previousValue;
    operator = value;
    currentInput = '';
    // Optionally show operator on display
    updateDisplay(value);
  }
}

// Attach event listeners to buttons
buttons.forEach(button => {
  const val = button.dataset.value;
  if (val !== undefined) {
    button.addEventListener('click', () => handleButton(val));
  }
});
