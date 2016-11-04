var gulp = require('gulp'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    rename = require('gulp-rename'),
    browserSync = require('browser-sync').create(),
    cssnano = require('gulp-cssnano');


gulp.task('css', function () {
    return gulp.src('scss/main.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer('last 4 version'))
    .pipe(gulp.dest('css'))
    .pipe(cssnano())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('css'))
    .pipe(browserSync.stream())
});

// Static Server + watching scss/html files
gulp.task('serve', ['css'], function() {

    browserSync.init({
        server: "./"
    });

    gulp.watch("scss/**/*.scss", ['css']);
    gulp.watch("*.html").on('change', browserSync.reload);
});

gulp.task('default', ['serve']);
