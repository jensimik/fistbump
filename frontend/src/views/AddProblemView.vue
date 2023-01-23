<template>
  <div class="flex one">
    <div>
      <h2>Add problem</h2>
    </div>
    <div>
      Awesome with a new problem 💪 let's add it
    </div>
    <div>
      <form>
        <label for="name">Name</label>
        <input type="text" required name="name" placeholder="give it a good name and tag the tape too" />
        <label for="grade">Grade</label>
        <select name="grade">
          <option value="">Green (let)</option>
          <option value="">Yellow (5b)</option>
          <option value="">Yellow (5b+)</option>
          <option value="">Yellow (5b-5b+)</option>
          <option value="">Blue (5c)</option>
          <option value="">Blue (6a)</option>
          <option value="">Blue (6a+)</option>
          <option value="">Blue (5c-6a+)</option>
          <option value="">Purple (6b)</option>
          <option value="">Purple (6b+)</option>
          <option value="">Purple (6b-6b+)</option>
          <option value="">Red (6c)</option>
          <option value="">Red (6c+)</option>
          <option value="">Red (6c-6c+)</option>
          <option value="">Brown (7a)</option>
          <option value="">Brown (7a+)</option>
          <option value="">Brown (7a-7a+)</option>
          <option value="">Black (7b)</option>
          <option value="">Black (7b+)</option>
          <option value="">Black (7c)</option>
          <option value="">Black (7b-7c)</option>
          <option value="">Mytical white (7c+-8c)</option>
        </select>
        <label for="section">Section</label>
        <select name="section">
          <option value="">Section1</option>
          <option value="">Section2</option>
          <option value="">Section3</option>
          <option value="">Section4</option>
          <option value="">Section5</option>
        </select>
        <button class="button">add</button>
      </form>
    </div>
  </div>
</template>