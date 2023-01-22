<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <table class="primary">
      <thead>
        <tr>
          <th></th>
          <th>Today</th>
          <th>Tomorrow</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Opening hours</td>
          <td>09:00-23:30</td>
          <td>10:00-21:00</td>
        </tr>
        <tr>
          <td>Calendar</td>
          <td>-</td>
          <td>18:00-19:30 junior kursus<br>19:30-20:00 letøvet kursus</td>
        </tr>
      </tbody>
    </table>


    <table class="primary">
      <thead>
        <tr>
          <th>Gym load</th>
          <th>Currently</th>
          <th>Today</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>People</td>
          <td>15</td>
          <td><img
              src="https://i0.wp.com/wonderoftech.com/wp-content/uploads/2020/06/Live-Visit-Data-versus-Popular-Times-Google-Maps.jpg?w=556&ssl=1"
              width="128" />
          </td>
        </tr>
      </tbody>
    </table>

    <table class="primary">
      <thead>
        <tr>
          <th>Feed/news</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>2023-01-22</td>
          <td>Stökt</td>
          <td>Planned expiration 7a+</td>
        </tr>
        <tr>
          <td>2023-01-20</td>
          <td>Stökt</td>
          <td>One Jump 7a</td>
        </tr>
        <tr>
          <td>2023-01-18</td>
          <td>Section1</td>
          <td>Blue problem 5c</td>
        </tr>
        <tr>
          <td>2023-01-16</td>
          <td>Section1</td>
          <td>Red problem 6c+</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>


<style scoped>
table.primary {
  width: 100%;
}
</style>