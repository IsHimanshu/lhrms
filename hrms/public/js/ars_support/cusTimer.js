
(function (win, $) {
  "use strict";
  if (!($ && $.fn && $.fn.datepicker)) return;

  
  function buildParser(format) {
    var map = {'dd':'(\\d{2})','d':'(\\d{1,2})','mm':'(\\d{2})','m':'(\\d{1,2})','yyyy':'(\\d{4})','yy':'(\\d{2})','hh':'(\\d{2})','h':'(\\d{1,2})','ii':'(\\d{2})','i':'(\\d{1,2})'};
    var order=[], esc=String(format||'').replace(/([.^$+?()[\]{}|])/g,'\\$1');
    var re=esc.replace(/(dd|d|mm|m|yyyy|yy|hh|h|ii|i)/g,function(tok){order.push(tok);return map[tok];});
    return { re:new RegExp('^'+re+'$'), order:order };
  }
  function parseWithFormat(str, fmt) {
    var p=buildParser(fmt), m=p.re.exec(String(str||'').trim()); if(!m) return null;
    var v={year:1970,month:1,date:1,hours:0,minutes:0};
    for (var i=0;i<p.order.length;i++){ var tok=p.order[i], val=parseInt(m[i+1],10);
      if(tok==='yyyy') v.year=val; else if(tok==='yy') v.year=2000+val;
      else if(tok==='mm'||tok==='m') v.month=val; else if(tok==='dd'||tok==='d') v.date=val;
      else if(tok==='hh'||tok==='h') v.hours=val; else if(tok==='ii'||tok==='i') v.minutes=val;
    }
    var mi=Math.max(1,Math.min(12,v.month))-1;
    var d=new Date(v.year,mi,Math.max(1,Math.min(31,v.date)),v.hours,v.minutes,0);
    d.setSeconds(0,0); return d;
  }
  function inferFormat($input){
    var fmt=$input.attr('data-parse-format'); if (fmt) return fmt;
    var inst=$input.data('datepicker'), o=inst && inst.opts;
    var df=o && (o.dateFormat || o.dateformat || o.date_format);
    var tf=o && (o.timeFormat || o.timeformat || o.time_format);
    if (df && tf) return df + (o.dateTimeSeparator || ' ') + tf;
    if (df) return df + ' hh:ii';
    return 'dd/mm/yyyy hh:ii';
  }
  function norm00(d){
    if (!(d instanceof Date)) d=new Date(d);
    if (!isNaN(+d)) d.setSeconds(0,0);
    return d;
  }
  function debounce(fn,ms){ var t; return function(){ var c=this,a=arguments; clearTimeout(t); t=setTimeout(function(){fn.apply(c,a);},ms);} }

  
  (function whenReady(cb){
    if ($.fn.datepicker.Timepicker) cb();
    else setTimeout(function(){ whenReady(cb); }, 40);
  })(function(){
    var TP = $.fn.datepicker.Timepicker;
    var DP = $.fn.datepicker.Constructor;

    
    var _build = TP.prototype._buildHTML;
    TP.prototype._buildHTML = function(){
      _build.call(this);
      this.seconds = 0; this.minSeconds = 0; this.maxSeconds = 0;
      if (this.$seconds && this.$seconds.length) this.$seconds.val(0);
      var $tp = this.$timepicker;
      if ($tp && $tp.length){
        $tp.find('.datepicker--time-row').eq(2).remove();               
        $tp.find('.datepicker--time-current-seconds').remove();          
        $tp.find('.datepicker--time-current-colon').last().remove();    
      }
    };
    var _updateCur = TP.prototype._updateCurrentTime;
    TP.prototype._updateCurrentTime = function(){
      this.seconds = 0;
      if (this.$seconds && this.$seconds.length) this.$seconds.val(0);
      _updateCur.call(this);
      this.$timepicker && this.$timepicker.find('.datepicker--time-current-seconds').text('00');
    };
    var _onChange = TP.prototype._onChangeRange;
    TP.prototype._onChangeRange = function(e){
      _onChange.call(this,e);
      this.seconds = 0;
      this.d && this.d._trigger && this.d._trigger('timeChange', [this.hours, this.minutes, 0]);
      this.update && this.update();
    };


    (function injectCSS(){
      var css =
        '.datepicker .datepicker--time .datepicker--time-row:nth-child(3){display:none!important;}' +
        '.datepicker .datepicker--time-current-seconds{display:none!important;}' +
        '.datepicker .datepicker--time-current-colon:last-child{display:none!important;}';
      var style=document.createElement('style'); style.type='text/css';
      style.appendChild(document.createTextNode(css)); document.head.appendChild(style);
    })();


    var _selectDate = DP.prototype.selectDate;
    DP.prototype.selectDate = function(date){
      try {
        if (Array.isArray(date)) date = date.map(norm00); else date = norm00(date);
      } catch(_){}
      return _selectDate.apply(this, arguments.length ? [date] : arguments);
    };


    var _show = DP.prototype.show;
    DP.prototype.show = function(){
      try {
        var $el = this.$el;
        if ($el && $el.length){
          var fmt = inferFormat($el);
          var d = parseWithFormat($el.val(), fmt);
          if (d) { try { this.selectDate(d); } catch(_){ } }
        }
      } catch(_){}
      return _show.apply(this, arguments);
    };

  
    function attachParser($input){
      if (!$input || !$input.length || $input.data('adpNoSecParseBound')) return;
      $input.data('adpNoSecParseBound', true);

      var applyParsed = function(){
        var fmt = inferFormat($input);
        var d = parseWithFormat($input.val(), fmt);
        if (!d) return;
        var inst = $input.data('datepicker');
        if (inst && typeof inst.selectDate === 'function') { try { inst.selectDate(d); } catch(_){} }
      };
      var applyParsedDeb = debounce(applyParsed, 250);

      $input
        .on('blur.adpParse', applyParsed)
        .on('change.adpParse', applyParsed)
        .on('keydown.adpParse', function(e){ if (e.key === 'Enter') applyParsed(); })
        .on('input.adpParse', applyParsedDeb);
    }

    
    $(document).on('focusin', '.datepicker-here', function(){
      var $t = $(this);
      if (!$t.data('datepicker')) { 
        try { $t.datepicker($t.data()); } catch(_){}
      }
      attachParser($t);
    });


    $(function(){
      $('.datepicker-here').each(function(){
        var $el = $(this);
        if ($el.data('datepicker')) attachParser($el);
      });
    });
  });
})(window, window.jQuery);
