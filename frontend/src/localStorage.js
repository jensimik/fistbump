import useLocalStorage from './useLocalStorage';

export const name = useLocalStorage("name", "");
export const setter_code = useLocalStorage("setter_code", "");
export const sections = useLocalStorage("sections", ["calendar", "hours_popular", "strip", "problems"]);
export const setter = useLocalStorage("setter", "no");
export const setter_auth = useLocalStorage("setter_auth", "");
