(function () {
  if (typeof SLUG === 'undefined') return;

  const display = document.getElementById('chordpro-display');
  if (!display) return;

  fetch('/assets/chordpro/' + SLUG + '.pro')
    .then(function (r) {
      if (!r.ok) throw new Error('not found');
      return r.text();
    })
    .then(function (text) {
      display.innerHTML = parseChordPro(text);
    })
    .catch(function () {
      display.innerHTML = '<p class="placeholder">Chord chart not available.</p>';
    });

  function escHtml(s) {
    return s
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function renderChordLine(line) {
    var parts = [];
    var firstBracket = line.indexOf('[');

    if (firstBracket > 0) {
      parts.push({ chord: '', lyric: line.substring(0, firstBracket) });
    }

    var re = /\[([^\]]+)\]([^\[]*)/g;
    var m;
    while ((m = re.exec(line)) !== null) {
      parts.push({ chord: m[1], lyric: m[2] });
    }

    // Screen: chords stacked above lyrics
    var html = '<div class="chord-line">';
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      var lyric = p.lyric.length ? escHtml(p.lyric) : '\u00a0';
      var chord = p.chord.length ? escHtml(p.chord) : '\u00a0';
      html += '<span class="chord-pair">';
      html += '<span class="chord">' + chord + '</span>';
      html += '<span class="lyric">' + lyric + '</span>';
      html += '</span>';
    }
    html += '</div>';

    // Print: chords inline with lyrics as [Chord]
    var inline = '';
    var re2 = /\[([^\]]+)\]([^\[]*)/g;
    if (firstBracket > 0) {
      inline += escHtml(line.substring(0, firstBracket));
    }
    while ((m = re2.exec(line)) !== null) {
      inline += '<span class="chord-inline">[' + escHtml(m[1]) + ']</span>' + escHtml(m[2]);
    }
    html += '<div class="inline-line">' + inline + '</div>';

    return html;
  }

  function parseChordPro(text) {
    var lines = text.split('\n');
    var html = '';
    var inVerse = false;
    var inChorus = false;

    function closeVerse() {
      if (inVerse) { html += '</div>'; inVerse = false; }
    }
    function closeChorus() {
      if (inChorus) { html += '</div>'; inChorus = false; }
    }

    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trimEnd();

      // {title:Song Name} — render as chart heading
      var titleMatch = line.match(/^\{title:([^}]*)\}/i);
      if (titleMatch) {
        html += '<div class="cp-title">' + escHtml(titleMatch[1].trim()) + '</div>';
        html += '<div class="cp-byline">by @seanmcgrathmusic</div>';
        continue;
      }

      // Skip key directive — already shown in song meta
      if (/^\{key:/i.test(line)) continue;

      // {comment:label} — visually distinct section label
      var commentMatch = line.match(/^\{comment:([^}]*)\}/i);
      if (commentMatch) {
        closeVerse();
        html += '<div class="cp-comment">' + escHtml(commentMatch[1].trim()) + '</div>';
        continue;
      }

      // {soc} / {start_of_chorus} — begin chorus block
      if (/^\{soc\}/i.test(line) || /^\{start_of_chorus\}/i.test(line)) {
        closeVerse();
        html += '<div class="chorus">';
        inChorus = true;
        continue;
      }

      // {eoc} / {end_of_chorus} — end chorus block
      if (/^\{eoc\}/i.test(line) || /^\{end_of_chorus\}/i.test(line)) {
        closeVerse();
        closeChorus();
        continue;
      }

      // {chorus} — repeat chorus marker (no content, just a label)
      if (/^\{chorus\}/i.test(line)) {
        closeVerse();
        html += '<div class="cp-comment cp-chorus-ref">Chorus</div>';
        continue;
      }

      // Other directives — skip
      if (/^\{[^}]+\}/.test(line)) continue;

      // Blank line — verse break
      if (line.trim() === '') {
        closeVerse();
        continue;
      }

      // Line with chords
      if (line.indexOf('[') !== -1) {
        if (!inVerse) { html += '<div class="verse">'; inVerse = true; }
        html += renderChordLine(line);
      } else {
        if (!inVerse) { html += '<div class="verse">'; inVerse = true; }
        html += '<div class="plain-line">' + escHtml(line) + '</div>';
      }
    }

    closeVerse();
    closeChorus();
    return html;
  }
})();
