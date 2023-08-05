//   MeCab -- Yet Another Part-of-Speech and Morphological Analyzer
//
//
//   Copyright(C) 2001-2006 Taku Kudo <taku@chasen.org>
//   Copyright(C) 2004-2006 Nippon Telegraph and Telephone Corporation

/* ----------------------------------------------------------------- */
/*           The Japanese TTS System "Open JTalk"                    */
/*           developed by HTS Working Group                          */
/*           http://open-jtalk.sourceforge.net/                      */
/* ----------------------------------------------------------------- */
/*                                                                   */
/*  Copyright (c) 2008-2016  Nagoya Institute of Technology          */
/*                           Department of Computer Science          */
/*                                                                   */
/* All rights reserved.                                              */
/*                                                                   */
/* Redistribution and use in source and binary forms, with or        */
/* without modification, are permitted provided that the following   */
/* conditions are met:                                               */
/*                                                                   */
/* - Redistributions of source code must retain the above copyright  */
/*   notice, this list of conditions and the following disclaimer.   */
/* - Redistributions in binary form must reproduce the above         */
/*   copyright notice, this list of conditions and the following     */
/*   disclaimer in the documentation and/or other materials provided */
/*   with the distribution.                                          */
/* - Neither the name of the HTS working group nor the names of its  */
/*   contributors may be used to endorse or promote products derived */
/*   from this software without specific prior written permission.   */
/*                                                                   */
/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND            */
/* CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,       */
/* INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF          */
/* MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          */
/* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS */
/* BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,          */
/* EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED   */
/* TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,     */
/* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON */
/* ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   */
/* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY    */
/* OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE           */
/* POSSIBILITY OF SUCH DAMAGE.                                       */
/* ----------------------------------------------------------------- */

#ifndef MECAB_ICONV_H
#define MECAB_ICONV_H

#if defined HAVE_ICONV
#include <iconv.h>
#endif

/* for Open JTalk
#if defined(_WIN32) && !defined(__CYGWIN__)
*/
#ifdef HAVE_WINDOWS_H /* for Open JTalk */
#include "windows.h"
#endif

namespace MeCab {

class Iconv {
 private:
#ifdef HAVE_ICONV
  iconv_t ic_;
#else
  int ic_;
#endif

/* for Open JTalk
#if defined(_WIN32) && !defined(__CYGWIN__)
*/
#ifdef HAVE_WINDOWS_H /* for Open JTalk */
  DWORD from_cp_;
  DWORD to_cp_;
#endif

 public:
  explicit Iconv();
  virtual ~Iconv();
  bool open(const char *from, const char *to);
  bool convert(std::string *);
};
}

#endif
