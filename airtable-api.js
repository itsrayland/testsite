// Airtable API Integration
const AIRTABLE_API_KEY = 'YOUR_API_KEY';
const AIRTABLE_BASE_ID = 'YOUR_BASE_ID';
const AIRTABLE_API_URL = `https://api.airtable.com/v0/${AIRTABLE_BASE_ID}`;

// API Headers
const headers = {
  'Authorization': `Bearer ${AIRTABLE_API_KEY}`,
  'Content-Type': 'application/json'
};

// Table Management
async function createTable(tableData) {
  try {
    const response = await fetch(`${AIRTABLE_API_URL}/tables`, {
      method: 'POST',
      headers,
      body: JSON.stringify(tableData)
    });
    return await response.json();
  } catch (error) {
    console.error('Error creating table:', error);
    throw error;
  }
}

async function updateTable(tableId, tableData) {
  try {
    const response = await fetch(`${AIRTABLE_API_URL}/tables/${tableId}`, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(tableData)
    });
    return await response.json();
  } catch (error) {
    console.error('Error updating table:', error);
    throw error;
  }
}

async function deleteTable(tableId) {
  try {
    const response = await fetch(`${AIRTABLE_API_URL}/tables/${tableId}`, {
      method: 'DELETE',
      headers
    });
    return await response.json();
  } catch (error) {
    console.error('Error deleting table:', error);
    throw error;
  }
}

// Field Management
async function createField(tableId, fieldData) {
  try {
    const response = await fetch(`${AIRTABLE_API_URL}/tables/${tableId}/fields`, {
      method: 'POST',
      headers,
      body: JSON.stringify(fieldData)
    });
    return await response.json();
  } catch (error) {
    console.error('Error creating field:', error);
    throw error;
  }
}

async function updateField(tableId, fieldId, fieldData) {
  try {
    const response = await fetch(`${AIRTABLE_API_URL}/tables/${tableId}/fields/${fieldId}`, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(fieldData)
    });
    return await response.json();
  } catch (error) {
    console.error('Error updating field:', error);
    throw error;
  }
}

async function deleteField(tableId, fieldId) {
  try {
    const response = await fetch(`${AIRTABLE_API_URL}/tables/${tableId}/fields/${fieldId}`, {
      method: 'DELETE',
      headers
    });
    return await response.json();
  } catch (error) {
    console.error('Error deleting field:', error);
    throw error;
  }
}

// Get Tables and Fields
async function getTables() {
  try {
    const response = await fetch(`${AIRTABLE_API_URL}/tables`, {
      headers
    });
    return await response.json();
  } catch (error) {
    console.error('Error getting tables:', error);
    throw error;
  }
}

async function getFields(tableId) {
  try {
    const response = await fetch(`${AIRTABLE_API_URL}/tables/${tableId}/fields`, {
      headers
    });
    return await response.json();
  } catch (error) {
    console.error('Error getting fields:', error);
    throw error;
  }
}

// Export API functions
export {
  createTable,
  updateTable,
  deleteTable,
  createField,
  updateField,
  deleteField,
  getTables,
  getFields
}; 