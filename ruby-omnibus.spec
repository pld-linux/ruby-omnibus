#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	omnibus
Summary:	Omnibus helps you build self-installing, full-stack software builds
Name:		ruby-%{pkgname}
Version:	1.3.0
Release:	1
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	731632866980ca85133c96ef5bc1e8a8
Patch0:		makeself-path.patch
Patch1:		omnibus-pld.patch
URL:		https://github.com/opscode/omnibus-ruby
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-rspec
BuildRequires:	ruby-rspec_junit_formatter
%endif
Requires:	ruby-fpm < 1.1
Requires:	ruby-fpm >= 1.0.0
Requires:	ruby-mixlib-config < 2.2
Requires:	ruby-mixlib-config >= 2.1.0
Requires:	ruby-mixlib-shellout < 1.4
Requires:	ruby-mixlib-shellout >= 1.3.0
Requires:	ruby-ohai >= 0.6.12
Requires:	ruby-rake >= 0.9
Requires:	ruby-thor >= 0.16.0
Requires:	ruby-uber-s3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Omnibus helps you build self-installing, full-stack software builds.

%prep
%setup -q -n %{pkgname}-%{version}
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*
%patch -P0 -p1
%patch -P1 -p1

# move these to libdir, so they don't clobber system bin dir
chmod a-x bin/makeself*
mv bin/makeself* lib/%{pkgname}

%build
# write .gemspec
%__gem_helper spec

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/omnibus
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
