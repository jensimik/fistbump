<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <table class="primary">
      <thead>
        <tr>
          <th colspan="2">Hours</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Today</td>
          <td>09:00-23:30</td>
        </tr>
        <tr>
          <td>Tomorrow</td>
          <td>10:00-21:00</td>
        </tr>
      </tbody>
    </table>


    <table class="primary">
      <thead>
        <tr>
          <th colspan="2">Calendar</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>18:00-19:30</td>
          <td>junior kursus</td>
        </tr>
        <tr>
          <td>19:30-20:00</td>
          <td>letøvet kursus</td>
        </tr>
      </tbody>
    </table>

    <table class="primary">
      <thead>
        <tr>
          <th colspan="2">Gym load</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Currently</td>
          <td>15</td>
        </tr>
        <tr>
          <td>Today</td>
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
          <th colspan="3">Feed/news</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>01-22</td>
          <td>S</td>
          <td>Planned expiration 7a+</td>
        </tr>
        <tr>
          <td>01-20</td>
          <td>S</td>
          <td>One Jump 7a</td>
        </tr>
        <tr>
          <td>01-18</td>
          <td>S1</td>
          <td>Blue problem 5c</td>
        </tr>
        <tr>
          <td>01-16</td>
          <td>S2</td>
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