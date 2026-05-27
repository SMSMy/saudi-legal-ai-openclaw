'use strict';

// ── Search index (Phase 1: skills, sources, prompts only) ──
const SEARCH_INDEX = [
  // Skills
  { type: 'skill',  title_ar: 'مراجعة العقود',               title_en: 'Contract Review',
    keywords: ['عقد','بنود','مراجعة','مخاطر','شرط جزائي','فسخ','contract','clause','review'],
    url: 'skills.html#contract-review' },
  { type: 'skill',  title_ar: 'النزاعات التجارية',           title_en: 'Commercial Dispute',
    keywords: ['نزاع','تجاري','محكمة تجارية','مطالبة','دعوى','commercial','dispute','court'],
    url: 'skills.html#commercial-dispute' },
  { type: 'skill',  title_ar: 'نظام التحكيم',                title_en: 'Arbitration',
    keywords: ['تحكيم','شرط تحكيم','محكم','arbitration','award'],
    url: 'skills.html#arbitration' },
  { type: 'skill',  title_ar: 'فحص الامتثال',                title_en: 'Compliance Check',
    keywords: ['امتثال','نطاقات','سعودة','PDPL','WPS','GOSI','compliance','nitaqat'],
    url: 'skills.html#compliance-check' },
  { type: 'skill',  title_ar: 'تحليل نظام العمل',            title_en: 'Labor Law Analysis',
    keywords: ['نظام العمل','عمالة','عقد عمل','مكافأة نهاية الخدمة','labor','employment'],
    url: 'skills.html#labor-law-analysis' },
  { type: 'skill',  title_ar: 'الصياغة القانونية',           title_en: 'Legal Drafting',
    keywords: ['صياغة','مذكرة','عريضة','إشعار','drafting','notice','memo'],
    url: 'skills.html#legal-drafting' },
  { type: 'skill',  title_ar: 'عقود العقارات والإيجار',      title_en: 'Real Estate Contracts',
    keywords: ['عقار','إيجار','ايجار','REGA','real estate','lease'],
    url: 'skills.html#real-estate-contracts' },

  // Official sources
  { type: 'source', title_ar: 'هيئة الخبراء بمجلس الوزراء',  title_en: 'Bureau of Experts (boe.gov.sa)',
    keywords: ['هيئة الخبراء','نص نظام','boe','bureau of experts'],
    url: 'https://www.boe.gov.sa' },
  { type: 'source', title_ar: 'الجريدة الرسمية — أم القرى',  title_en: 'Official Gazette (uqn.gov.sa)',
    keywords: ['أم القرى','جريدة رسمية','مرسوم ملكي','official gazette','uqn'],
    url: 'https://www.uqn.gov.sa' },
  { type: 'source', title_ar: 'ناجز — وزارة العدل',           title_en: 'Najiz — Ministry of Justice',
    keywords: ['ناجز','وزارة العدل','قضاء','تنفيذ','najiz','justice'],
    url: 'https://www.najiz.sa' },
  { type: 'source', title_ar: 'وزارة الموارد البشرية',        title_en: 'Ministry of Human Resources (hrsd.gov.sa)',
    keywords: ['موارد بشرية','وزارة العمل','hrsd','human resources'],
    url: 'https://www.hrsd.gov.sa' },
  { type: 'source', title_ar: 'منصة قيوة',                   title_en: 'Qiwa Platform',
    keywords: ['قيوة','عقود عمل','رخص العمل','qiwa','work permit'],
    url: 'https://www.qiwa.sa' },
  { type: 'source', title_ar: 'منصة استطلاع',                title_en: 'Istitlaa — Public Consultation',
    keywords: ['استطلاع','مشاورة عامة','مسودة أنظمة','istitlaa','consultation'],
    url: 'https://www.istitlaa.gov.sa' },
  { type: 'source', title_ar: 'هيئة حماية البيانات الشخصية', title_en: 'Personal Data Protection Authority',
    keywords: ['PDPL','حماية البيانات','خصوصية','pdpa','data protection'],
    url: 'https://www.pdpa.gov.sa' },
  { type: 'source', title_ar: 'الهيئة العامة للعقار',         title_en: 'Real Estate General Authority (rega.gov.sa)',
    keywords: ['عقار','REGA','تسجيل عقاري','real estate authority'],
    url: 'https://www.rega.gov.sa' },

  // Prompts
  { type: 'prompt', title_ar: 'قالب مراجعة عقد',              title_en: 'Contract Review Prompt',
    keywords: ['مراجعة عقد','تحليل عقد','contract review','prompt'],
    url: 'templates.html' },
  { type: 'prompt', title_ar: 'قالب صياغة إشعار قانوني',     title_en: 'Draft Legal Notice Prompt',
    keywords: ['إشعار','إنذار','مطالبة','legal notice','draft'],
    url: 'templates.html' },
  { type: 'prompt', title_ar: 'قالب تحليل المخاطر القانونية', title_en: 'Legal Risk Analysis Prompt',
    keywords: ['مخاطر','تحليل قانوني','تقييم مخاطر','risk analysis'],
    url: 'templates.html' },
];

const TYPE_LABELS = {
  skill:  { ar: 'مهارة', cls: 'result-type-skill'  },
  source: { ar: 'مصدر',  cls: 'result-type-source' },
  prompt: { ar: 'قالب',  cls: 'result-type-prompt' },
};

// ── DOM wiring (runs after defer) ──
const searchInput    = document.getElementById('search-input');
const searchDropdown = document.getElementById('search-dropdown');

if (searchInput && searchDropdown) {
  searchInput.addEventListener('input', onInput);
  searchInput.addEventListener('keydown', onKeydown);
  document.addEventListener('click', onClickOutside);
}

function onInput() {
  const query = searchInput.value.trim();
  if (query.length < 2) { hideDropdown(); return; }
  renderDropdown(runSearch(query));
}

function runSearch(query) {
  const q = query.toLowerCase();
  return SEARCH_INDEX.filter(item =>
    item.title_ar.toLowerCase().includes(q) ||
    item.title_en.toLowerCase().includes(q) ||
    item.keywords.some(k => k.toLowerCase().includes(q))
  ).slice(0, 6);
}

// ── Safe DOM rendering (no innerHTML with dynamic content) ──
function renderDropdown(results) {
  while (searchDropdown.firstChild) {
    searchDropdown.removeChild(searchDropdown.firstChild);
  }

  if (results.length === 0) {
    const msg = document.createElement('div');
    msg.className = 'search-no-result';

    msg.appendChild(document.createTextNode('لا توجد نتائج مطابقة — تصفّح '));

    const sourcesLink = document.createElement('a');
    sourcesLink.href = 'sources.html';
    sourcesLink.textContent = 'المصادر';
    msg.appendChild(sourcesLink);

    msg.appendChild(document.createTextNode(' أو '));

    const skillsLink = document.createElement('a');
    skillsLink.href = 'skills.html';
    skillsLink.textContent = 'المهارات';
    msg.appendChild(skillsLink);

    msg.appendChild(document.createTextNode(' مباشرةً.'));

    searchDropdown.appendChild(msg);
    showDropdown();
    return;
  }

  results.forEach(item => {
    const type = TYPE_LABELS[item.type] || { ar: item.type, cls: '' };
    const isExternal = item.url.startsWith('http');

    const link = document.createElement('a');
    link.className = 'search-result';
    link.href = item.url;
    if (isExternal) { link.target = '_blank'; link.rel = 'noopener'; }
    link.setAttribute('role', 'option');

    const badge = document.createElement('span');
    badge.className = 'result-type ' + type.cls;
    badge.textContent = type.ar;

    const textWrap = document.createElement('span');
    textWrap.className = 'result-text';

    const titleAr = document.createElement('span');
    titleAr.className = 'result-title-ar';
    titleAr.textContent = item.title_ar;

    const titleEn = document.createElement('span');
    titleEn.className = 'result-title-en';
    titleEn.setAttribute('dir', 'ltr');
    titleEn.textContent = item.title_en;

    textWrap.appendChild(titleAr);
    textWrap.appendChild(titleEn);
    link.appendChild(badge);
    link.appendChild(textWrap);
    searchDropdown.appendChild(link);
  });

  showDropdown();
}

function showDropdown() {
  searchDropdown.classList.add('visible');
  searchInput.setAttribute('aria-expanded', 'true');
}

function hideDropdown() {
  searchDropdown.classList.remove('visible');
  searchInput.setAttribute('aria-expanded', 'false');
}

function onClickOutside(e) {
  if (!e.target.closest('#search-wrap')) { hideDropdown(); }
}

function onKeydown(e) {
  if (e.key === 'Escape') { hideDropdown(); searchInput.blur(); }
}
