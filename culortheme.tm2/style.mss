// Languages: name (local), name_en, name_fr, name_es, name_de
@name: '[name_en]';

// Fonts //
@sans: 'Source Sans Pro Regular';
@sans_italic: 'Source Sans Pro Italic';
@sans_bold: 'Source Sans Pro Semibold';

// Color1 #B19F6E
// Color2 #453328
// Color3 #B09993
// Color4 #796F6D
// Color5 #452322

// Common Colors //
@land: #FFFFFF;
@water: #B09993;

Map { background-color: @land; }

// Political boundaries //

#admin[admin_level=2][maritime=0] {
  line-join: round;
  line-color: #453328;
  line-width: 1.4;
  [zoom>=6] { line-width: 2; }
  [zoom>=8] { line-width: 4; }
  [disputed=1] { line-dasharray: 4,4; }
}


#building [zoom>=16]{
::wall { polygon-fill: #453328; }
::roof {
  polygon-fill: #B09993;
  polygon-geometry-transform:translate(-1,-1);
  polygon-clip:false;  
  line-width: 0.25;
  line-color: mix(@land, #000, 85);
  line-geometry-transform:translate(-1,-1);
  line-clip:false;
  [zoom>=17] {
    line-width:0.5;
  }
    [zoom>=18] {
      polygon-geometry-transform:translate(-1,-2);
        line-geometry-transform:translate(-1,-2);
      line-width:0.75;
    }
 }
}


// Places //

#country_label[zoom>=3] {
  text-name: @name;
  text-face-name: @sans_bold;
  text-fill: #452322;
  text-size: 12;
  [zoom>=3][scalerank=1],
  [zoom>=4][scalerank=2],
  [zoom>=5][scalerank=3],
  [zoom>=6][scalerank>3] {
    text-size: 14;
  }
  [zoom>=4][scalerank=1],
  [zoom>=5][scalerank=2],
  [zoom>=6][scalerank=3],
  [zoom>=7][scalerank>3] {
    text-size: 16;
  }
}

#country_label_line { line-color: fadeout(#452322,75%); }

#place_label[localrank<=2] {
  [type='city'][zoom<=15] {
    text-name: @name;
    text-face-name: @sans_bold;
    text-fill: #452322;
    text-size: 16;
    [zoom>=10] { text-size: 18; }
    [zoom>=12] { text-size: 24; }
  }
  [type='town'][zoom<=17] {
    text-name: @name;
    text-face-name: @sans;
    text-fill:#452322;
    text-size: 14;
    [zoom>=10] { text-size: 16; }
    [zoom>=12] { text-size: 20; }
  }
  [type='village'] {
    text-name: @name;
    text-face-name: @sans;
    text-fill: #452322;
    text-size: 12;
    [zoom>=12] { text-size: 14; }
    [zoom>=14] { text-size: 18; }
  }
  [type='hamlet'],
  [type='suburb'],
  [type='neighbourhood'] {
    text-name: @name;
    text-face-name: @sans;
    text-fill: #452322;
    text-size: 12;
    [zoom>=14] { text-size: 14; }
    [zoom>=16] { text-size: 16; }
  }
}

// Water Features //

#water {
  polygon-fill: @water;
  polygon-gamma: 0.6;
}

#water_label {
  [zoom<=13],  // automatic area filtering @ low zooms
  [zoom>=14][area>500000],
  [zoom>=16][area>10000],
  [zoom>=17] {
    text-name: @name;
    text-face-name: @sans_italic;
    text-fill: darken(@water, 30%);
    text-size: 13;
    text-wrap-width: 100;
    text-wrap-before: true;
  }
}

#waterway {
  [type='river'],
  [type='canal'] {
    line-color: @water;
    line-width: 0.5;
    [zoom>=12] { line-width: 1; }
    [zoom>=14] { line-width: 2; }
    [zoom>=16] { line-width: 3; }
  }
  [type='stream'] {
    line-color: @water;
    line-width: 0.5;
    [zoom>=14] { line-width: 1; }
    [zoom>=16] { line-width: 2; }
    [zoom>=18] { line-width: 3; }
  }
}

// Roads & Railways //

#tunnel { opacity: 0.5; }

#road,
#tunnel,
#bridge {
  ['mapnik::geometry_type'=2] {
    line-color: #B19F6E;
    line-width: 0.5;
    [class='motorway'],
    [class='main'] {
      [zoom>=10] { line-width: 1; }
      [zoom>=12] { line-width: 2; }
      [zoom>=14] { line-width: 3; }
      [zoom>=16] { line-width: 5; }
    }
    [class='street'],
    [class='street_limited'] {
      [zoom>=14] { line-width: 1; }
      [zoom>=16] { line-width: 2; }
    }
    [class='street_limited'] { line-dasharray: 4,1; }
  }
}
