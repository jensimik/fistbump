import { useLocalStorage } from './useLocalStorage';

export default {
    name: useLocalStorage("name", ""),
    setter_code: useLocalStorage("setter_code", ""),
    sections: useLocalStorage("sections", ["calendar", "hours_popular", "strip", "problems"]),
    setter: useLocalStorage("setter", "no"),
    setter_auth: useLocalStorage("setter_auth", ""),
}