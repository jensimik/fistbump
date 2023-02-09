import useLocalStorage from './useLocalStorage';

export const name = useLocalStorage("name", "");
export const setter_code = useLocalStorage("setter_code", "");
export const sections = useLocalStorage("sections", ["calendar", "hours_popular", "strip", "problems"]);
export const setter = useLocalStorage("setter", "no");
export const setter_auth = useLocalStorage("setter_auth", "");

// problems filters
export const filter_search_text = useLocalStorage("filter_search_text", "");
export const filter_sections = useLocalStorage("filter_sections", ["S1", "S2", "S3", "S4", "S5", "Ö"]);
export const filter_grades = useLocalStorage("filter_grades", ["green", "yellow", "blue", "purple", "red", "brown", "black", "turquoise"]);
export const filter_gridview = useLocalStorage("filter_gridview", true);

// recent problems filters
export const filter_rp_sections = useLocalStorage("filter_rp_sections", ["B", "Ö"]);
export const filter_rp_grades = useLocalStorage("filter_rp_grades", ["green", "yellow", "blue", "purple", "red", "brown", "black", "turquoise"]);
