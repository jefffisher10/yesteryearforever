// 🎲 Random Post Button
const pages = [ "absdbs", "adena_rover", "backyard_astronomy", "brief_morning_walk", "cardboard_computer", "celestial_oceans_and_islands", "cell_tower_dystopia", "changing_your_mind", "code_ode", "cosmic_scale", "creepy_crawlies_to_quasars", "different_perspective", "explorers_and_innovators", "fallout_4_was_made_for_me", "fisher_observatory", "friday_the_13th", "fundamental_meaning", "goonies_treasure_map_replica", "great_american_eclipse", "green_lamp", "hands_on_nature", "hopewell_v1-0", "hopewell_v1-5", "identity", "impossible_picture", "innocence_ending", "junkbot_alpha", "lie_down", "music_projects", "nature-tech_romance", "nature_happy_place", "nomads_sky", "orbits_for_dummies", "play_with_your_food", "primal_astronomy", "puppet_monster", "puzzle_box", "second_star_to_the_right", "six_planet_infograph", "spaceship_cross-section", "the_a_i_scare", "tic-tac-toe_BASH", "turtle_feeder", "virus_mutation_simulation", "white_whale", "why_i_love_stargazing", "yellow_house_recording_studio", "your_own_path" ]; // ← overwritten by update.py

function goRandom() {
  const random = pages[Math.floor(Math.random() * pages.length)];
  window.location.href = "/" + random + ".html";
}


document.addEventListener("DOMContentLoaded", function () {

  // 🌙 Dark Mode Toggle
  const toggle = document.getElementById("toggle-dark-mode");

  if (toggle) {
    toggle.addEventListener("click", () => {
      document.body.classList.toggle("dark");
      localStorage.setItem("darkMode", document.body.classList.contains("dark"));
    });

    if (localStorage.getItem("darkMode") === "true") {
      document.body.classList.add("dark");
    }
  }


  // 🔍 Lightbox
  const imgs = document.querySelectorAll('.thumbnail, .post-image');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');

  imgs.forEach(img => {
    img.addEventListener('click', () => {
      const fullSrc = img.dataset.full || img.src;
      lightboxImg.src = fullSrc;
      lightbox.style.display = 'flex';
    });
  });

  if (lightbox) {
    lightbox.addEventListener('click', () => {
      lightbox.style.display = 'none';
      lightboxImg.src = '';
    });
  }


  // 🎵 Audio Playlist
  document.querySelectorAll('[id$="-tracklist"]').forEach(tracklist => {
    const albumId = tracklist.id.replace('-tracklist', '');
    const player = document.getElementById(albumId + '-player');

    if (!player) return;

    tracklist.addEventListener('click', function(e) {
      if (e.target.tagName.toLowerCase() === 'a' && e.target.dataset.src) {
        e.preventDefault();
        player.src = e.target.dataset.src;
        player.play();
        tracklist.querySelectorAll('a').forEach(a => a.style.fontWeight = "");
        e.target.style.fontWeight = "bold";
      }
    });
  });

});
